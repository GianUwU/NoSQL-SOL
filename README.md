# NoSQL-SOL
Selbst Organisiertes Lernen Schulauftrag

## 1.1 ODM

ODM steht für **Object Document Mapper**. Es ist das Gegenstück zum ORM (Object Relational Mapper), wird aber für dokumentenbasierte Datenbanken wie MongoDB verwendet.

Ein ODM kümmert sich darum, dass Dokumente aus der Datenbank auf Objekte im Code gemappt werden. So kann man direkt mit Klassen arbeiten, anstatt mit rohen Dictionaries oder JSON-Strukturen.

Beispiele für Python-ODMs sind **MongoEngine** und **Beanie**. PyMongo selbst ist kein ODM, es ist ein Treiber (Driver), der direkte Datenbankzugriffe ermöglicht, aber kein automatisches Mapping übernimmt.
