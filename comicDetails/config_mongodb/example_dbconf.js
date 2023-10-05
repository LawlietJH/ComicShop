db = db.getSiblingDB('configuraciones_appcom');
db.getCollection('configuraciones').findOne({ "_id": "idDelDocumento" });
db.getCollection('configuraciones').updateOne({ "_id": "idDelDocumento" },
    {
        $set: {
            "endpoint": true,
            "configuracion": {
                "ejemplo": "ejemplo"
            }
        }
    },
    { "multi": false, "upsert": false });
db.getCollection('configuraciones').findOne({ "_id": "idDelDocumento" });