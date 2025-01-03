/* 

DO $$ 
DECLARE
    obj RECORD;
BEGIN
    -- Drop all foreign key constraints
    FOR obj IN
        SELECT conname, connamespace::regnamespace::text, conrelid::regclass::text
        FROM pg_constraint
        WHERE contype = 'f'  -- 'f' indicates foreign key
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
        EXECUTE format('DROP TABLE IF EXISTS %I.%I CASCADE', 'public', obj.tablename);
    END LOOP;

    -- Drop all sequences
    FOR obj IN
        SELECT sequencename
        FROM pg_sequences
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP SEQUENCE IF EXISTS %I.%I CASCADE', 'public', obj.sequencename);
    END LOOP;

    -- Drop all views
    FOR obj IN
        SELECT viewname
        FROM pg_views
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP VIEW IF EXISTS %I.%I CASCADE', 'public', obj.viewname);
    END LOOP;

    -- Drop all materialized views
    FOR obj IN
        SELECT matviewname
        FROM pg_matviews
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP MATERIALIZED VIEW IF EXISTS %I.%I CASCADE', 'public', obj.matviewname);
    END LOOP;

    -- Drop all functions
    FOR obj IN
        SELECT routine_name
        FROM information_schema.routines
        WHERE routine_schema = 'public'
    LOOP
        EXECUTE format('DROP FUNCTION IF EXISTS %I.%I() CASCADE', 'public', obj.routine_name);
    END LOOP;

    -- Drop all types
    FOR obj IN
        SELECT typname
        FROM pg_type
        WHERE typnamespace = 'public'::regnamespace
          AND typtype = 'e'  -- 'e' indicates an enum type
    LOOP
        EXECUTE format('DROP TYPE IF EXISTS %I.%I CASCADE', 'public', obj.typname);
    END LOOP;

    -- Drop all indexes (other than constraints, which are handled above)
    FOR obj IN
        SELECT indexname
        FROM pg_indexes
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP INDEX IF EXISTS %I.%I CASCADE', 'public', obj.indexname);
    END LOOP;

END $$;

*/