DO $$
BEGIN
    -- Drop all foreign key constraints
    PERFORM (
        SELECT COALESCE(string_agg(format(
            'ALTER TABLE %I.%I DROP CONSTRAINT %I;',
            nspname, relname, conname), ' '), '')
        FROM pg_constraint
        JOIN pg_class ON pg_constraint.conrelid = pg_class.oid
        JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid
        WHERE contype = 'f'
    );

    -- Drop all tables
    PERFORM (
        SELECT COALESCE(string_agg(format('DROP TABLE IF EXISTS %I.%I CASCADE;', schemaname, tablename), ' '), '')
        FROM pg_tables
        WHERE schemaname = 'public'
    );

    -- Drop all sequences
    PERFORM (
        SELECT COALESCE(string_agg(format('DROP SEQUENCE IF EXISTS %I.%I CASCADE;', schemaname, sequencename), ' '), '')
        FROM pg_sequences
        WHERE schemaname = 'public'
    );

    -- Drop all views
    PERFORM (
        SELECT COALESCE(string_agg(format('DROP VIEW IF EXISTS %I.%I CASCADE;', schemaname, viewname), ' '), '')
        FROM pg_views
        WHERE schemaname = 'public'
    );

    -- Drop all materialized views
    PERFORM (
        SELECT COALESCE(string_agg(format('DROP MATERIALIZED VIEW IF EXISTS %I.%I CASCADE;', schemaname, matviewname), ' '), '')
        FROM pg_matviews
        WHERE schemaname = 'public'
    );

    -- Drop all functions
    PERFORM (
        SELECT COALESCE(string_agg(format('DROP FUNCTION IF EXISTS %I.%I(%s) CASCADE;', n.nspname, p.proname, pg_get_function_identity_arguments(p.oid)), ' '), '')
        FROM pg_proc p
        JOIN pg_namespace n ON p.pronamespace = n.oid
        WHERE n.nspname = 'public'
    );

    -- Drop all types
    PERFORM (
        SELECT COALESCE(string_agg(format('DROP TYPE IF EXISTS %I.%I CASCADE;', n.nspname, t.typname), ' '), '')
        FROM pg_type t
        JOIN pg_namespace n ON t.typnamespace = n.oid
        WHERE n.nspname = 'public' AND t.typtype = 'e'
    );

    -- Reset the schema to default state
    EXECUTE 'DROP SCHEMA IF EXISTS public CASCADE';
    EXECUTE 'CREATE SCHEMA public';
    EXECUTE 'GRANT ALL ON SCHEMA public TO postgres';
    EXECUTE 'GRANT ALL ON SCHEMA public TO public';
END $$;