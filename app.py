#!/usr/bin/env python3

from aws_cdk import core

from dms_mongodb_to_documentdb.dms_mongodb_to_documentdb_stack import DmsMongodbToDocumentdbStack


app = core.App()
DmsMongodbToDocumentdbStack(app, "dms-mongodb-to-documentdb")

app.synth()
