## Run Alembic Migrations

### Configuration

```bash
cp alembic.ini.example alembic.ini
```

- Update the `alembic.ini` file with your database credentials (`sqlalchemy.url`).

### Create a new migration (Optional)

```bash
alembic revision --autogenerate -m "migration message"
```

### Upgrade the database

```bash
alembic upgrade head
```
