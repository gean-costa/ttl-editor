# ttl-editor

## Subir arquivo no Fuseki

* URI: **http://vocabularies.unesco.org/thesaurus/th1**
* Arquivo: **data/th1.ttl**

## Adicionar ao `config.ttl`:

```
# Skosmos vocabularies

:opentheso a skosmos:Vocabulary, void:Dataset ;
    dc:title "Opentheso Thesaurus"@en ;
    skosmos:shortName "opentheso";
    dc:subject :cat_general ;
    void:uriSpace "http://vocabularies.unesco.org/thesaurus/th1";
    skosmos:language "en", "es", "fr", "ru", "pt";
    skosmos:defaultLanguage "en";
    skosmos:showTopConcepts true ;
    skosmos:fullAlphabeticalIndex true ;
    skosmos:groupClass skos:Collection ;
    void:sparqlEndpoint <http://localhost:3030/skosmos/sparql> ;
    skosmos:sparqlGraph <http://vocabularies.unesco.org/thesaurus/th1> .
```