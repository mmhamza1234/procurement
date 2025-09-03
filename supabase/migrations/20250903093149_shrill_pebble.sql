/*
  # Hamada Tool Database Schema

  1. New Tables
    - `user_activities` - Logs all user interactions for analytics and AI training
    - `terms_acceptance` - Tracks terms and conditions acceptance
    - `supplier_data` - Stores supplier information with full audit trail
    - `processed_documents` - Stores document processing results
    - `generated_emails` - Stores email generation history

  2. Security
    - Enable RLS on all tables
    - Add policies for anonymous access (tool doesn't require authentication)
    - Create indexes for performance

  3. Analytics
    - Create views for usage statistics
    - Add functions for data analysis
*/

-- Create user_activities table for comprehensive logging
CREATE TABLE IF NOT EXISTS user_activities (
    id BIGSERIAL PRIMARY KEY,
    activity_type VARCHAR(100) NOT NULL,
    data JSONB NOT NULL,
    user_id VARCHAR(100) DEFAULT 'anonymous',
    session_id VARCHAR(100),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    tool_version VARCHAR(50) DEFAULT 'hamada_tool_v1.0',
    ip_address INET,
    user_agent TEXT
);

-- Create terms_acceptance table
CREATE TABLE IF NOT EXISTS terms_acceptance (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    session_id VARCHAR(100),
    terms_version VARCHAR(20) NOT NULL DEFAULT '1.0',
    acceptance_timestamp TIMESTAMPTZ DEFAULT NOW(),
    data_collection_consent BOOLEAN DEFAULT TRUE,
    ip_address INET,
    user_agent TEXT,
    acceptance_method VARCHAR(50) DEFAULT 'web_form'
);

-- Create supplier_data table for backend storage
CREATE TABLE IF NOT EXISTS supplier_data (
    id BIGSERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    address TEXT,
    country VARCHAR(100),
    specialization TEXT,
    established_year INTEGER,
    material_categories TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(100) DEFAULT 'hamada_tool',
    is_active BOOLEAN DEFAULT TRUE
);

-- Create processed_documents table
CREATE TABLE IF NOT EXISTS processed_documents (
    id BIGSERIAL PRIMARY KEY,
    document_name VARCHAR(255),
    document_type VARCHAR(50),
    document_size BIGINT,
    extracted_text TEXT,
    extracted_materials JSONB,
    extracted_deadline DATE,
    extracted_specifications JSONB,
    project_name VARCHAR(255),
    tender_reference VARCHAR(255),
    processing_timestamp TIMESTAMPTZ DEFAULT NOW(),
    user_id VARCHAR(100) DEFAULT 'anonymous',
    session_id VARCHAR(100)
);

-- Create generated_emails table
CREATE TABLE IF NOT EXISTS generated_emails (
    id BIGSERIAL PRIMARY KEY,
    project_name VARCHAR(255),
    tender_reference VARCHAR(255),
    supplier_company VARCHAR(255),
    supplier_email VARCHAR(255),
    supplier_country VARCHAR(100),
    email_subject TEXT,
    email_body TEXT,
    material_categories JSONB,
    generation_timestamp TIMESTAMPTZ DEFAULT NOW(),
    user_id VARCHAR(100) DEFAULT 'anonymous',
    session_id VARCHAR(100),
    order_id VARCHAR(100)
);

-- Create order_tracking table
CREATE TABLE IF NOT EXISTS order_tracking (
    id BIGSERIAL PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE NOT NULL,
    project_name VARCHAR(255),
    tender_reference VARCHAR(255),
    materials JSONB,
    total_suppliers INTEGER DEFAULT 0,
    emails_sent INTEGER DEFAULT 0,
    supplier_categories TEXT,
    status VARCHAR(100) DEFAULT 'Pending Response',
    follow_up_date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    user_id VARCHAR(100) DEFAULT 'anonymous'
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_activities_timestamp ON user_activities(timestamp);
CREATE INDEX IF NOT EXISTS idx_user_activities_type ON user_activities(activity_type);
CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activities_session ON user_activities(session_id);

CREATE INDEX IF NOT EXISTS idx_terms_acceptance_user_id ON terms_acceptance(user_id);
CREATE INDEX IF NOT EXISTS idx_terms_acceptance_timestamp ON terms_acceptance(acceptance_timestamp);

CREATE INDEX IF NOT EXISTS idx_supplier_data_company ON supplier_data(company_name);
CREATE INDEX IF NOT EXISTS idx_supplier_data_country ON supplier_data(country);
CREATE INDEX IF NOT EXISTS idx_supplier_data_active ON supplier_data(is_active);

CREATE INDEX IF NOT EXISTS idx_processed_documents_timestamp ON processed_documents(processing_timestamp);
CREATE INDEX IF NOT EXISTS idx_processed_documents_project ON processed_documents(project_name);

CREATE INDEX IF NOT EXISTS idx_generated_emails_timestamp ON generated_emails(generation_timestamp);
CREATE INDEX IF NOT EXISTS idx_generated_emails_project ON generated_emails(project_name);

CREATE INDEX IF NOT EXISTS idx_order_tracking_order_id ON order_tracking(order_id);
CREATE INDEX IF NOT EXISTS idx_order_tracking_status ON order_tracking(status);

-- Enable Row Level Security
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE terms_acceptance ENABLE ROW LEVEL SECURITY;
ALTER TABLE supplier_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE processed_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_emails ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_tracking ENABLE ROW LEVEL SECURITY;

-- Create policies for anonymous access (since tool doesn't require authentication)
CREATE POLICY "Allow anonymous read access" ON user_activities
    FOR SELECT USING (true);

CREATE POLICY "Allow anonymous insert" ON user_activities
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow anonymous read access" ON terms_acceptance
    FOR SELECT USING (true);

CREATE POLICY "Allow anonymous insert" ON terms_acceptance
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow anonymous access" ON supplier_data
    FOR ALL USING (true);

CREATE POLICY "Allow anonymous access" ON processed_documents
    FOR ALL USING (true);

CREATE POLICY "Allow anonymous access" ON generated_emails
    FOR ALL USING (true);

CREATE POLICY "Allow anonymous access" ON order_tracking
    FOR ALL USING (true);

-- Create comprehensive analytics views
CREATE OR REPLACE VIEW usage_analytics AS
SELECT 
    DATE(timestamp) as activity_date,
    activity_type,
    COUNT(*) as activity_count,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT session_id) as unique_sessions
FROM user_activities
GROUP BY DATE(timestamp), activity_type
ORDER BY activity_date DESC, activity_count DESC;

CREATE OR REPLACE VIEW daily_summary AS
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as total_activities,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT session_id) as unique_sessions,
    COUNT(CASE WHEN activity_type = 'document_processed' THEN 1 END) as documents_processed,
    COUNT(CASE WHEN activity_type = 'email_generated' THEN 1 END) as emails_generated,
    COUNT(CASE WHEN activity_type = 'supplier_searched' THEN 1 END) as supplier_searches,
    COUNT(CASE WHEN activity_type = 'deadline_calculated' THEN 1 END) as deadline_calculations,
    COUNT(CASE WHEN activity_type = 'order_tracked' THEN 1 END) as order_updates,
    COUNT(CASE WHEN activity_type = 'terms_accepted' THEN 1 END) as terms_acceptances
FROM user_activities
GROUP BY DATE(timestamp)
ORDER BY date DESC;

CREATE OR REPLACE VIEW supplier_analytics AS
SELECT 
    country,
    COUNT(*) as supplier_count,
    COUNT(CASE WHEN is_active = true THEN 1 END) as active_suppliers,
    STRING_AGG(DISTINCT material_categories, ', ') as all_materials
FROM supplier_data
GROUP BY country
ORDER BY supplier_count DESC;

-- Create functions for advanced analytics
CREATE OR REPLACE FUNCTION get_activity_summary(days_back INTEGER DEFAULT 30)
RETURNS TABLE (
    activity_type VARCHAR(100),
    total_count BIGINT,
    unique_users BIGINT,
    unique_sessions BIGINT,
    avg_per_day NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ua.activity_type,
        COUNT(*) as total_count,
        COUNT(DISTINCT ua.user_id) as unique_users,
        COUNT(DISTINCT ua.session_id) as unique_sessions,
        ROUND(COUNT(*)::NUMERIC / days_back, 2) as avg_per_day
    FROM user_activities ua
    WHERE ua.timestamp >= NOW() - INTERVAL '1 day' * days_back
    GROUP BY ua.activity_type
    ORDER BY total_count DESC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_recent_activity(limit_count INTEGER DEFAULT 20)
RETURNS TABLE (
    activity_type VARCHAR(100),
    user_id VARCHAR(100),
    session_id VARCHAR(100),
    timestamp TIMESTAMPTZ,
    data JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ua.activity_type,
        ua.user_id,
        ua.session_id,
        ua.timestamp,
        ua.data
    FROM user_activities ua
    ORDER BY ua.timestamp DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_usage_trends(days_back INTEGER DEFAULT 30)
RETURNS TABLE (
    date DATE,
    total_activities BIGINT,
    unique_users BIGINT,
    documents_processed BIGINT,
    emails_generated BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        DATE(ua.timestamp) as date,
        COUNT(*) as total_activities,
        COUNT(DISTINCT ua.user_id) as unique_users,
        COUNT(CASE WHEN ua.activity_type = 'document_processed' THEN 1 END) as documents_processed,
        COUNT(CASE WHEN ua.activity_type = 'email_generated' THEN 1 END) as emails_generated
    FROM user_activities ua
    WHERE ua.timestamp >= NOW() - INTERVAL '1 day' * days_back
    GROUP BY DATE(ua.timestamp)
    ORDER BY date DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to sync CSV supplier data to database
CREATE OR REPLACE FUNCTION sync_supplier_data()
RETURNS INTEGER AS $$
DECLARE
    sync_count INTEGER := 0;
BEGIN
    -- This function can be called to sync CSV data to the database
    -- Implementation would depend on how you want to handle the sync
    RETURN sync_count;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_supplier_data_updated_at
    BEFORE UPDATE ON supplier_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_order_tracking_updated_at
    BEFORE UPDATE ON order_tracking
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon;

-- Insert initial data for testing (optional)
INSERT INTO user_activities (activity_type, data, user_id, session_id) VALUES 
('system_initialized', '{"message": "Hamada Tool database initialized", "version": "1.0"}', 'system', 'init_session')
ON CONFLICT DO NOTHING;