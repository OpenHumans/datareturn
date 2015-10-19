# datareturn
Give individuals access to S3-hosted data files, also exportable to Open Humans.

Individuals are managed according to their email addresses. The email is what the account is initialized for, files are returned to that address, and login tokens go to it.

## Admin set up

* Use `virtualenv` and install requirements with pip
(`pip install requirements.txt`).
* Have `foreman` installed. Foreman is used to load environment variables,
which is how you'll store your private AWS keys.
* Migrations: `python manage.py migrate`
* Use 'createsuperuser' to create a new admin account for yourself with
`python manage.py createsuperuser`
* Use this account to log in to the admin site at `/admin`. Edit the "Site"
object so the "domain name" and "display name" are the names you would like to
use for this site. Create a "SiteConfig" object for the "Site" object and enter
the associated information.
* Follow instructions for ["Loading files into S3"](https://github.com/PersonalGenomesOrg/datareturn#loading-files-into-s3)
* Create user accounts with associated data by running: `foreman run python manage.py load_data`
* You can download a CSV listing your users (by email address) and a fresh set of associated login tokens by visiting `/admin/user_tokens`. This is useful for sending
out an email notifying these individuals of their new accounts and data.

### Loading files into S3

* Copy `env.example` to `.env` and add info needed for using AWS S3
* Create a CSV format document with these features [(see example)](https://github.com/PersonalGenomesOrg/datareturn/blob/master/example/examplelist.csv):
  * No header
  * First column: Individual's email address
  * Second column: `local` (currently only option)
  * Third column: Local path to the file
  * Fourth column: Name to give the file in S3 and on the site
* To load these files onte S3, use foreman to run `scripts/load_files.py`, e.g.: `foreman run python scripts/load_files.py FILELIST.CSV --localpath FILE/PATH/`

For example, running the following in the project's base directory (which uses the example list ["examplelist.csv"](https://github.com/PersonalGenomesOrg/datareturn/blob/master/example/examplelist.csv)
and data in the ["exampledata" directory](https://github.com/PersonalGenomesOrg/datareturn/tree/master/example/exampledata/):
* `foreman run python scripts/load_files.py example/examplelist.csv --localpath example/exampledata`

...results in the S3 file loaded with this key:
* `datareturn/862f0de367ce252edd509bd25a3505c91d0e145a/photo.jpg`

###
