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
  * **Column 1: Recipient.**<br>The recipient's email address.
  * **Column 2: Type.**<br>There are two different types of data return: `file` or `link`.
  * **Column 3: Path to file.**
    * for `link`: URL to return.
    * for `file`: local file that will be loaded onto S3.<br>
    _(Note: the version of this file uploaded onto S3 will have this
      field replaced with the S3 key name.)_
  * **Column 4: Name.**
    * for `file`: the basename to use for the file on S3.
    * for `link`: a name to use when displaying the link.
  * **Column 5: Description.**<br>Description of this item.
* To load these files onte S3, use foreman to run `scripts/load_files.py`, e.g.:<br>`foreman run python scripts/load_files.py FILELIST.CSV --localpath FILE/PATH/`

For example, running the following in the project's base directory (which uses the example list ["examplelist.csv"](https://github.com/PersonalGenomesOrg/datareturn/blob/master/example/examplelist.csv)
and data in the ["exampledata" directory](https://github.com/PersonalGenomesOrg/datareturn/tree/master/example/exampledata/):
* `foreman run python scripts/load_files.py example/examplelist.csv --localpath example/exampledata`

...results in:
*  an S3 file loaded with the key `datareturn/862f0de367ce252edd509bd25a3505c91d0e145a/photo.jpg`
* a slightly modified version of `examplelist.csv` loaded to S3 with the key ``datareturn_info.csv``

###
