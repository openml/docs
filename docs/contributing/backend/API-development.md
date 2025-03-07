!!! tip "Phasing out"
    This documentation is about the old PHP-based API, which wil be phased out in favor of (e.g. [the new Python-based API (using FastAPI)](https://github.com/openml/server-api)). See the 'Server' tab for more information.


## Important resources

REST API docs: www.openml.org/apis

Controller: https://github.com/openml/OpenML/blob/master/openml_OS/controllers/Api_new.php

Models: https://github.com/openml/OpenML/tree/master/openml_OS/models/api/v1

Templates: https://github.com/openml/OpenML/tree/master/openml_OS/views/pages/api_new/v1

## Golden Rules for Development

1. **Code Maintainability before anything else**. The code has to be understandable, and if not conflicting with that, short. Avoid code duplications as much as possible.
2. The API controller is the only entity giving access to the API models. Therefore, the responsibility for API access can be handled by the controller
3. Read-Only operations are of the type GET. Operations that make changes in the database are of type POST or DELETE. Important, because this is the way the controller determines to allow users with a given set of privileges to access functions.
4. Try to avoid direct queries to the database. Instead, use the respective models functions: 'get()', 'getWhere()', 'getById()', insert(), etc (Please make yourself familiar with the basic model: [read-only](https://github.com/openml/website/blob/master/openml_OS/models/abstract/Database_read.php) and [write](https://github.com/openml/website/blob/master/openml_OS/models/abstract/Database_write.php))
5. No external program/script execution during API calls (with one exception: data split generation). This makes the API unnecessarily slow, hard to debug and vulnerable to crashes. If necessary, make a cronjob that executes the program / script

## Backend code structure

The high-level architecture of the website, including the controllers for different parts of the website (REST API, html, ...) and connections to the database.

### Code

The source code is available in the 'OpenML' repository:
https://github.com/openml/OpenML 

### Important files and folders

In this section we go through all important files and folder of the
system.

#### Root directory

The root directory of OpenML contains the following files and folders.

- **system**: This folder contains all files provided by
  CodeIgniter 2.1.3. The contents of this folder is
  beyond the scope of this document, and not relevant for extending
  OpenML. All the files in this folder are in the same state as they
  were provided by Ellislabs, and none of these files should ever be
  changed.

- **sparks**: Sparks is a package management system for
  Codeigniter that allows for instant installation of libraries into
  the application. This folder contains two libraries provided by
  third party software developers, oauth1 (based on version 1 the
  oauth protocol) and oauth2 (similarly, based on version 2 of the
  oauth protocol). The exact contents of this folder is beyond the
  scope of this document and not relevant for extending OpenML.

- **openml_OS**: All files in this folder are written specifically
  for OpenML. When extending the functionality OpenML, usually one of
  the files in this folder needs to be adjusted. As a thorough
  understanding of the contents of this folder is vital for extending
  OpenML, we will discuss the contents of this folder in
  [[URL Mapping]] in more detail.

- **index.php**: This is the “bootstrap” file of the system.
  Basically, every page request on OpenML goes through this file (with
  the css, images and javascript files as only exception). It then
  determines which CodeIgniter and OpenML files need to be included.
  This file should not be edited.

- **.htaccess**: This file (which configures the Apache Rewrite
  Engine) makes sure that all URL requests will be directed to
  `index.php`. Without this file, we would need to include `index.php`
  explicitly in every URL request. This file makes sure that all other
  URL requests without `index.php` embedded in it automatically will
  be transformed to `index.php`. Eg.,
  <http://www.openml.org/frontend/page/home> will be rewritten to
  <http://www.openml.org/index.php/frontend/page/home>. This will be
  explained in detail in [[URL Mapping]].

- **css**: A folder containing all stylesheets. These are important
  for the layout of OpenML.

- **data**: A folder containing data files, e.g., datasets,
  implementation files, uploaded content. Please note that this folder
  does not necessarily needs to be present in the root directory. The
  OpenML Base Config file determines the
  exact location of this folder.

- **downloads**: Another data folder, containing files like the most
  recent database snapshot.

- **img**: A folder containing all static images shown on the webpage.

- **js**: A folder containing all used Javascript files and libraries,
  including third party libraries like jQuery and datatables.

- Various other files, like .gitignore, favicon.ico, etc.

#### openml_OS

This folder is (in CodeIgniter jargon) the “Application folder”, and
contains all files relevant to OpenML. Within this folder, the following
folders should be present: (And also some other folders, but these are
not used by OpenML)

- **config**: A folder containing all config files. Most notably, it
  contains the file <span>BASE_CONFIG.php</span>, in which all system
  specific variables are set; the config items within this file
  differs over various installations (e.g., on localhost,
  `openml.org`). Most other config files, like
  <span>database.php</span>, will receive their values from
  <span>BASE_CONFIG.php</span>. Other important config files are
  <span>autoload.php</span>, determining which CodeIgniter / OpenML
  files will be loaded on any request, <span>openML.php</span>,
  containing config items specific to OpenML, and
  <span>routes.php</span>, which will be explained in
  [[URL Mapping]].

- **controllers**: In the Model/View/Controller design pattern, all
  user interaction goes through controllers. In a webapplication
  setting this means that every time a URL gets requested, exactly one
  controller gets invoked. The exact dynamics of this will be
  explained in [[URL Mapping]].

- **core**: A folder that contains CodeIgniter specific files. These
  are not relevant for the understanding of OpenML.

- **helpers**: This folder contains many convenience functions.
  Wikipedia states: “A convenience function is a non-essential
  subroutine in a programming library or framework which is intended
  to ease commonly performed tasks”. For example the
  <span>file_upload_helper.php</span> contains many functions that
  assist with uploading of files. Please note that a helper function
  must be explicitly loaded in either the autoload config or the files
  that uses its functions.

- **libraries**: Similar to sparks, this folder contains libraries
  specifically written for CodeIgniter. For example, the library used
  for all user management routines is in this folder.

- **models**: In the Model/View/Controller design pattern, models
  represent the state of the system. In a webapplication setting, you
  could say that a model is the link to the database. In OpenML,
  almost all tables of the database are represented by a model. Each
  model has general functionality applicable to all models (e.g.,
  retrieve all records, retrieve record with constraints, insert
  record) and functionality specific to that model (e.g., retrieve a
  dataset that has certain data properties). Most models extend an
  (abstract) base class, located in the <span>abstract</span> folder.
  This way, all general functionality is programmed and maintained in
  one place.

- **third_party**: Although the name might suggests differently, this
  folder contains all OpenML Java libraries.

- **views**: In the Model/View/Controller design pattern, the views
  are the way information is presented on the screen. In a
  webapplication setting, a view usually is a block of (PHP generated)
  HTML code. The most notable view is <span>frontend_main.php</span>,
  which is the template file determining the main look and feel of
  OpenML. Every single page also has its own specific view (which is
  parsed within <span>frontend_main.php</span>). These pages can be
  found (categorized by controller and name) in the <span>pages</span>
  folder. More about this structure is explained in
  [[URL Mapping]].

## Frontend code structure

Architecture and libraries involved in generating the frontend functions.

Code: https://github.com/openml/website/tree/master/openml_OS/views

### High-level

All pages are generated by first loading _frontend_main.php_. This creates the 'shell' in which the content is loaded. It loads all css and javascript libraries, and contains the html for displaying headers and footers.

### Create new page

The preferred method is creating a new folder into the folder
`<root_directory>/openml_OS/views/pages/frontend`
This page can be requested by
`http://www.openml.org/frontend/page/<folder_name>`
or just
`http://www.openml.org/<folder_name>`
This method is preferred for human readable webpages, where the internal
actions are simple, and the output is complex. We will describe the
files that can be in this folder.

- **pre.php**: Mandatory file. Will be executed first. Do not make
  this file produce any output! Can be used to pre-render data, or set
  some variables that are used in other files.

- **body.php**: Highly recommended file. Intended for displaying the
  main content of this file. Will be rendered at the right location
  within the template file (`frontend_main.php`).

- **javascript.php**: Non-mandatory file. Intended for javascript
  function on which `body.php` relies. Will be rendered within a
  javascript block in the header of the page.

- **post.php**: Non mandatory file. Will only be executed when a POST
  request is done (e.g., when a HTML form was send using the POST
  protocol). Will be executed after `pre.php`, but before the
  rendering process (and thus, before `body.php` and
  `javascript.php`). Should handle the posted input, e.g., file
  uploads.

It is also recommended to add the newly created folder to the mapping in
the `routes.php` config file. This way it can also be requested by the
shortened version of the URL. (Note that we deliberately avoided to
auto-load all pages into this file using a directory scan, as this makes
the webplatform slow.)

## URL to Page Mapping

Most pages in OpenML are represented by a folder in
<root_directory>/openml_OS/views/pages/frontend
The contents of this folder will be parsed in the template
`frontend_main.php` template, as described in [[backend]]. In
this section we explain the way an URL is mapped to a certain OpenML
page.

### URL Anatomy

By default, CodeIgniter (and OpenML) accepts a URL in the following
form:
`http://www.openml.org/index.php/<controller>/<function>/<p1>/<pN>/<free>`
The various parts in the URL are divided by slashes. Every URL starts
with the protocol and server name (in the case of OpenML this is
`http://www.openml.org/`). This is followed by the bootstrap file, which
is always the same, i.e., `index.php`. The next part indicates the
controller that needs to be invoked; typically this is `frontend`,
`rest_api` or `data`, but it can be any file from the `openml_OS` folder
`controllers`. Note that the suffix `.php` should not be included in the
URL.

The next part indicates which function of the controller should be
invoked. This should be a existing, public function from the controller
that is indicated in the controller part. These functions might have one
or more parameters that need to be set. This is the following part of
the URL (indicated by `p1` and `pN`). The parameters can be followed by
anything in free format. Typically, this free format is used to pass on
additional parameters in `name` - `value` format, or just a way of
adding a human readable string to the URL for SEO purposes.

For example, the following URL
`http://www.openml.org/index.php/frontend/page/home` invokes
the function `page` from the `frontend` controller and sets the only
parameter of this function, `$indicator`, to value `home`. The function
`page` loads the content of the specified folder (`$indicator`) into the
main template. In this sense, the function `page` can be seen as some
sort of specialized page loader.

### URL Shortening

Since it is good practice to have URL’s as short as possible, we have
introduced some logic that shortens the URL’s. Most importantly, the URL
part that invokes `index.php` can be removed at no cost, since this file
is **always** invoked. For this, we use Apache’s rewrite engine. Rules
for rewriting URL’s can be found in the `.htaccess` file, but is
suffices to say that any URL in the following format
`http://www.openml.org/index.php/<controller>/<function>/<params>`
can due to the rewrite engine also be requested with
`http://www.openml.org/<controller>/<function>/<params>`

Furthermore, since most of the pages are invoked by the function `page`
of the `frontend` controller (hence, they come with the suffix
`frontend/page/page_name`) we also created a mapping that maps URL’s in
the following form
`http://www.openml.org/<page_name>`
to
`http://www.openml.org/frontend/page/<page_name>`
Note that Apache’s rewrite engine will also add `index.php` to this. The
exact mapping can be found in `routes.php` config file.

### Additional Mappings

Additionally, a mapping is created from the following type of URL:
`http://www.openml.org/api/<any_query_string>`
to
`http://www.openml.org/rest_api/<any_query_string>`
This was done for backwards compatibility. Many plugins make calls to
the not-existing `api` controller, which are automatically redirected to
the `rest_api` controller.

### Exceptions

It is important to note that not all pages do have a specific page
folder. The page folders are a good way of structuring complex GUI’s
that need to be presented to the user, but in cases where the internal
state changes are more important than the GUI’s, it might be preferable
to make the controller function print the output directly. This happens
for example in the functions of `rest_api.php` and `free_query.php`
(although the former still has some files in the views folder that it
refers to).

## XSD Schemas

In order to ensure data integrity on the server, data that passed to upload functions is checked against XSD schema's. This ensures that the data that is uploaded is in the correct format, and does not contain any illegal characters. XSD schema's can be obtained through the API (exact links are provided in the API docs, but for example: https://www.openml.org/api/v1/xsd/openml.data.upload (where openml.data.upload can be replaced by any other schema's name). Also XML examples are provided, e.g., https://www.openml.org/api/v1/xml_example/data . The XSD schema's are exactly the same as used on the server. Whenever an upload fails and the server mentions an XML/XSD verification error, please run the uploaded xml against one of the provided XSD schema's, for example on this webtool: http://www.freeformatter.com/xml-validator-xsd.html

In order to maintain one XSD schema for both uploading and downloading stuff, the XSD sometimes contains more fields than seem necessary from the offset. Usually, the additional fields that are indicated as such in the comments (for example, in the upload dataset xsd this are the id, upload_date, etc fields).
The XSD's maintain basically three consistencies functions:

- Ensure that the correct fields are uploaded
- Ensure that the fields contain the correct data types.
- Ensure that the fields do not contain to much characters for the database to upload.

For the latter two, it is important to note that the XSD seldom accept default string content (i.e., xs:string). Rather, we use self defined data types, that use regular expressions to ensure the right content. Examples of these are oml:system_string128, oml:casual_string128, oml:basic_latin128, where the oml prefix is used, the name indicates the level of restriction and the number indicates the maximum size of the field.

IMPORTANT: The maximum field sizes are (often) chosen with great care. Do not extend them without consulting other team members.

## User authentication

Authentication towards the server goes by means of a so-called api_key (a hexa-decimal string which uniquely identifies a user). Upon interaction with the server, the client passes this api_key to the server, and the server checks the rights of the user. Currently this goes by means of a get or post variable, but in the future we might want to use a header field (because of security). It is recommended to refresh your api_key every month.

IMPORTANT: Most authentication operations are handled by the ION_Auth library (http://benedmunds.com/ion_auth/). DO NOT alter information directly in the user table, always use the ION_Auth API.

A user can be part of one or many groups. The following user groups exists:

1. Admin Group: With great power comes great responsibility. Admin users can overrule all security checks on the server, i.e., delete a dataset or run that is not theirs, or even delete a flow that contains runs.
2. Normal Group: Level that is required for read/write interaction with the server. Almost all users are part of this group.
3. Read-only Group: Level that can be used for read interaction with the server. If a user is part of this group, but not part of 'Normal Group', he is allowed to download content, but can not upload or delete content.
4. Backend Group: (Work in Progress) Level that has more privileges than 'Normal Group'. Can submit Data Qualities and Evaluations.

The ION_Auth functions in_group(), add_to_group(), remove_from_group() and get_users_groups() are key towards interaction with these tables.

