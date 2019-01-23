from lxml import etree as ET


class TeiReader():

    """ a class to read an process tei-documents"""

    def __init__(self, xml):
        self.ns_tei = {'tei': "http://www.tei-c.org/ns/1.0"}
        self.ns_xml = {'xml': "http://www.w3.org/XML/1998/namespace"}
        self.nsmap = {
            'tei': "http://www.tei-c.org/ns/1.0",
            'xml': "http://www.w3.org/XML/1998/namespace",
            'tcf': "http://www.dspin.de/data/textcorpus"
        }
        self.file = xml
        try:
            self.original = ET.parse(self.file)
        except Exception as e:
            print(e)
            self.original = ET.fromstring(self.file)
        try:
            self.tree = ET.parse(self.file)
        except Exception as e:
            print(e)
            self.tree = ET.fromstring(self.file)
        try:
            self.parsed_file = ET.tostring(self.tree, encoding="utf-8")
        except Exception as e:
            print(e)
            self.parsed_file = "parsing didn't work"

    def replace_child_nodes(self, xpath_to_parent, new_child_nodes):
        children_xpath = "{}/tei:*".format(xpath_to_parent)
        parent_node = self.tree.xpath(xpath_to_parent, namespaces=self.ns_tei)[0]
        for x in self.tree.xpath(children_xpath, namespaces=self.ns_tei):
            x.getparent().remove(x)
        for y in new_child_nodes:
            parent_node.append(y)

        return self.tree

    def addr_lines(self):
        return self.tree.xpath('//tei:addrLine', namespaces=self.ns_tei)

    def extract_md(self):
        authors = self.tree.xpath(
            '//tei:titleStmt//tei:author', namespaces=self.ns_tei
        )
        title = self.tree.xpath(
            '//tei:titleStmt/tei:title//text()', namespaces=self.ns_tei
        )
        text_type = self.tree.xpath(
            '//tei:keywords[@n="subcategory"]/tei:term/text()', namespaces=self.ns_tei
        )
        keywords = self.tree.xpath(
            '//tei:keywords[@n="keywords"]/tei:term/text()', namespaces=self.ns_tei
        )
        topics = self.tree.xpath(
            '//tei:keywords[@n="topics"]/tei:term/text()', namespaces=self.ns_tei
        )
        md = {}
        md['authors'] = []
        md['nr_of_authors'] = len(authors)
        for x in authors:
            pers = {}
            for y in ["forename", "surname", "affiliation", "email"]:
                expr = './/tei:{}/text()'.format(y)
                nodeset = pers[y] = x.xpath(expr, namespaces=self.ns_tei)
                if len(nodeset) == 1:
                    pers[y] = nodeset[0]
                elif len(nodeset) > 1:
                    pers[y] = " ".join(nodeset)
                else:
                    pers[y] = None
            md['authors'].append(pers)
        if len(title) == 1:
            md['title'] = title[0].strip()
        elif len(title) > 1:
            md['title'] = " ".join(title).strip()
        md['text_type'] = text_type[0]
        md['keywords'] = keywords
        md['topics'] = [x.strip() for x in topics]
        md['fulltext'] = " ".join(
            self.tree.xpath(
                './/tei:body//text()',
                namespaces=self.ns_tei
            )
        )
        md['affils'] = len(
            set(
                self.tree.xpath(
                    './/tei:author//tei:affiliation/text()',
                    namespaces=self.ns_tei
                )
            )
        )
        return md
