# plants_photos

This script renames photos according to ids of plants in the database and sets its filenames to `photo_name` column.

## usage

1. Unpack archive containing photos named with plants russian names to `plants_photos` directory
2. Run `python update_photos`
3. Run `docker compose up` to start a server with photos.