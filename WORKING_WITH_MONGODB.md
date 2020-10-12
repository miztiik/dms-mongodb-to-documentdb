# Working with MongoDB on EC2 & Customize it

1.  ## 🔬 Troubleshooting

    ```bash
    # Stop/(re)Start Mongo Daemon
    sudo systemctl restart mongod

    # List all Database
    show dbs
    # Use one of the datbases
    use miztiik_db
    db.stats()
    # List all collections
    show collections
    # List some items
    db.customers.find()
    # List indexes
    db.customers.getIndexes()

    # For doing CDC, we need oplog enabled in MongoDB
    # https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MongoDB.html
    # https://docs.mongodb.com/manual/core/replica-set-oplog/

    # Check Status of Oplog
    rs.printReplicationInfo()

    # Troubleshooting Mongo Replication
    use local
    rs.conf()
    db.oplog.rs.stats()
    db.oplog.rs.find();

    # Verify Replication Configuration
    rs.conf()
    rs.status()

    ```

    ```json
    { "errmsg": "replication not detected" }
    ```

    ```bash
    # Stop Mongo Daemon

    sudo systemctl stop mongod
    sudo service mongod stop
    # Start Mongo Daemon with Replicaset enabled
    # sudo mongod --replSet "rs0" --dbpath /var/lib/mongo --auth -port 27017 &


    # In case you want to drop any database
    use miztiik_db
    db.dropDatabase()
    # or Drop collections ( in this case 'customers' )
    db.customers.drop
    ```

## 📌 Who is using this

This repository aims to teach api best practices to new developers, Solution Architects & Ops Engineers in AWS. Based on that knowledge these Udemy [course #1][103], [course #2][102] helps you build complete architecture in AWS.

### 💡 Help/Suggestions or 🐛 Bugs

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional documentation or solutions, we greatly value feedback and contributions from our community. [Start here][200]

### 👋 Buy me a coffee

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Q5Q41QDGK) Buy me a [coffee ☕][900].

### 📚 References

1. [Setup MongoDB Community Edition on EC2][1]

1. [Create Database in MongoDB][2]

1. [Create Index in Mongodb][3]

1. [Setup MongoDB for public access][4]

1. [Pymongo Insert][5]

1. [Pymongo Insert][6]

### 🏷️ Metadata

**Level**: 300

![miztiik-success-green](https://img.shields.io/badge/miztiik-success-green)

[1]: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-amazon/
[2]: https://www.mongodb.com/basics/create-database
[3]: https://www.guru99.com/working-mongodb-indexes.html
[4]: https://ianlondon.github.io/blog/mongodb-auth/
[5]: https://pythonexamples.org/python-mongodb-insert-document/
[6]: https://www.codespeedy.com/create-collections-and-insert-data-to-collection-in-mongodb-python/
[100]: https://www.udemy.com/course/aws-cloud-security/?referralCode=B7F1B6C78B45ADAF77A9
[101]: https://www.udemy.com/course/aws-cloud-security-proactive-way/?referralCode=71DC542AD4481309A441
[102]: https://www.udemy.com/course/aws-cloud-development-kit-from-beginner-to-professional/?referralCode=E15D7FB64E417C547579
[103]: https://www.udemy.com/course/aws-cloudformation-basics?referralCode=93AD3B1530BC871093D6
[200]: https://github.com/miztiik/api-with-stage-variables/issues
[899]: https://www.udemy.com/user/n-kumar/
[900]: https://ko-fi.com/miztiik
[901]: https://ko-fi.com/Q5Q41QDGK
