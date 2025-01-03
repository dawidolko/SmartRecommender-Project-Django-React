/* 

DO $$ 
DECLARE
    obj RECORD;
BEGIN
    -- Drop all foreign key constraints
    FOR obj IN
        SELECT conname, connamespace::regnamespace::text, conrelid::regclass::text
        FROM pg_constraint
        WHERE contype = 'f'
    LOOP
        EXECUTE format(
            'ALTER TABLE %I.%I DROP CONSTRAINT %I',
            obj.connamespace,
            obj.conrelid,
            obj.conname
        );
    END LOOP;

    -- Drop all tables
    FOR obj IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP TABLE IF EXISTS %I CASCADE', obj.tablename);
    END LOOP;

    -- Drop all sequences
    FOR obj IN
        SELECT sequencename
        FROM pg_sequences
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP SEQUENCE IF EXISTS %I CASCADE', obj.sequencename);
    END LOOP;

    -- Drop all views
    FOR obj IN
        SELECT viewname
        FROM pg_views
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP VIEW IF EXISTS %I CASCADE', obj.viewname);
    END LOOP;

    -- Drop all materialized views
    FOR obj IN
        SELECT matviewname
        FROM pg_matviews
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP MATERIALIZED VIEW IF EXISTS %I CASCADE', obj.matviewname);
    END LOOP;

    -- Drop all functions
    FOR obj IN
        SELECT routine_name
        FROM information_schema.routines
        WHERE routine_schema = 'public'
    LOOP
        EXECUTE format('DROP FUNCTION IF EXISTS %I() CASCADE', obj.routine_name);
    END LOOP;

    -- Drop all types
    FOR obj IN
        SELECT typname
        FROM pg_type
        WHERE typnamespace = 'public'::regnamespace
          AND typtype = 'e'
    LOOP
        EXECUTE format('DROP TYPE IF EXISTS %I CASCADE', obj.typname);
    END LOOP;
END $$;

*/