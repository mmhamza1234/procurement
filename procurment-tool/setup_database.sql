-- Database setup script for Hamada Tool
-- Run this in your Supabase SQL editor

-- Create user_activities table for logging user interactions
CREATE TABLE IF NOT EXISTS user_activities (
    id BIGSERIAL PRIMARY KEY,
    activity_type VARCHAR(100) NOT NULL,
    data JSONB NOT NULL,
    user_id VARCHAR(100) DEFAULT 'anonymous',
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    tool_version VARCHAR(50) DEFAULT 'hamada_tool_v1.0'
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_user_activities_timestamp ON user_activities(timestamp);
CREATE INDEX IF NOT EXISTS idx_user_activities_type ON user_activities(activity_type);
CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id);

-- Create terms_acceptance table for tracking terms acceptance
CREATE TABLE IF NOT EXISTS terms_acceptance (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    terms_version VARCHAR(20) NOT NULL,
    acceptance_timestamp TIMESTAMPTZ DEFAULT NOW(),
    data_collection_consent BOOLEAN DEFAULT TRUE,
    ip_address INET,
    user_agent TEXT
);

-- Create index for terms acceptance
CREATE INDEX IF NOT EXISTS idx_terms_acceptance_user_id ON terms_acceptance(user_id);
CREATE INDEX IF NOT EXISTS idx_terms_acceptance_timestamp ON terms_acceptance(acceptance_timestamp);

-- Create usage_statistics view for dashboard
CREATE OR REPLACE VIEW usage_statistics AS
SELECT 
    DATE(timestamp) as activity_date,
    activity_type,
    COUNT(*) as activity_count,
    COUNT(DISTINCT user_id) as unique_users
FROM user_activities
GROUP BY DATE(timestamp), activity_type
ORDER BY activity_date DESC, activity_count DESC;

-- Create daily_summary view
CREATE OR REPLACE VIEW daily_summary AS
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as total_activities,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(CASE WHEN activity_type = 'document_processed' THEN 1 END) as documents_processed,
    COUNT(CASE WHEN activity_type = 'email_generated' THEN 1 END) as emails_generated,
    COUNT(CASE WHEN activity_type = 'supplier_searched' THEN 1 END) as supplier_searches,
    COUNT(CASE WHEN activity_type = 'deadline_calculated' THEN 1 END) as deadline_calculations,
    COUNT(CASE WHEN activity_type = 'order_tracked' THEN 1 END) as order_updates
FROM user_activities
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Enable Row Level Security (RLS)
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE terms_acceptance ENABLE ROW LEVEL SECURITY;

-- Create policies for user_activities table
CREATE POLICY "Allow anonymous read access" ON user_activities
    FOR SELECT USING (true);

CREATE POLICY "Allow anonymous insert" ON user_activities
    FOR INSERT WITH CHECK (true);

-- Create policies for terms_acceptance table
CREATE POLICY "Allow anonymous read access" ON terms_acceptance
    FOR SELECT USING (true);

CREATE POLICY "Allow anonymous insert" ON terms_acceptance
    FOR INSERT WITH CHECK (true);

-- Create function to get activity summary
CREATE OR REPLACE FUNCTION get_activity_summary(days_back INTEGER DEFAULT 30)
RETURNS TABLE (
    activity_type VARCHAR(100),
    total_count BIGINT,
    unique_users BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ua.activity_type,
        COUNT(*) as total_count,
        COUNT(DISTINCT ua.user_id) as unique_users
    FROM user_activities ua
    WHERE ua.timestamp >= NOW() - INTERVAL '1 day' * days_back
    GROUP BY ua.activity_type
    ORDER BY total_count DESC;
END;
$$ LANGUAGE plpgsql;

-- Create function to get recent activity
CREATE OR REPLACE FUNCTION get_recent_activity(limit_count INTEGER DEFAULT 10)
RETURNS TABLE (
    activity_type VARCHAR(100),
    user_id VARCHAR(100),
    timestamp TIMESTAMPTZ,
    data JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ua.activity_type,
        ua.user_id,
        ua.timestamp,
        ua.data
    FROM user_activities ua
    ORDER BY ua.timestamp DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Insert sample data for testing (optional)
-- INSERT INTO user_activities (activity_type, data, user_id) VALUES 
-- ('document_processed', '{"file_name": "sample.pdf", "extracted_deadlines": 2}', 'test_user'),
-- ('email_generated', '{"project_name": "Sample Project", "supplier_count": 5}', 'test_user'),
-- ('supplier_searched', '{"materials": ["piping", "valves"], "results_count": 15}', 'test_user');

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon;