TEI_NSMAP = {
    'tei': "http://www.tei-c.org/ns/1.0",
    'xml': "http://www.w3.org/XML/1998/namespace",
}

tei_gen_header = """
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
         <titleStmt>
            <title type="main">{}</title>
            <title type="sub">{}</title>
         </titleStmt>
         <publicationStmt>
            <p/>
         </publicationStmt>
         <sourceDesc>
            <p></p>
         </sourceDesc>
        </fileDesc>
    </teiHeader>
    <text>
        <body/>
    </text>
</TEI>
"""
