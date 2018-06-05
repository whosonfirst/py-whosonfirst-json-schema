# py-whosonfirst-json-schema

Python tools for doing JSON Schema related things with Who's On First property definitions.

## Global install

```
$ sudo pip install -r requirements.txt .
```

## Virtualenv install

```
$ cd py-whosonfirst-json-schema
$ virtualenv .
$ source ./bin/activate
$ pip install -e .
...
$ deactivate
```

## Usage

Autogenerate `whosonfirst-json-schema/schema/docs/wof-properties.json` from `whosonfirst-properties`.

```
$ ./scripts/wof-build-schema /path/to/whosonfirst-properties > /path/to/whosonfirst-json-schema/schema/docs/wof-properties.json
```

## See also

* https://github.com/whosonfirst/whosonfirst-json-schema
* https://github.com/whosonfirst/whosonfirst-properties
