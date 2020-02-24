from lxml import etree as ET
from slugify import slugify

from lobid_utils import get_place_of_business_info


class TeiReader():

    """ a class to read an process tei-documents"""

    def __init__(self, xml):
        self.ns_tei = {'tei': "http://www.tei-c.org/ns/1.0"}
        self.ns_xml = {'xml': "http://www.w3.org/XML/1998/namespace"}
        self.ns_tcf = {'tcf': "http://www.dspin.de/data/textcorpus"}
        self.nsmap = {
            'tei': "http://www.tei-c.org/ns/1.0",
            'xml': "http://www.w3.org/XML/1998/namespace",
            'tcf': "http://www.dspin.de/data/textcorpus"
        }
        self.file = xml
        try:
            self.original = ET.parse(self.file)
        except Exception as e:
            print('could not parse file')
            try:
                self.original = ET.fromstring(self.file.encode('utf8'))
                print('read string worked')
            except Exception as e:
                print('read from string did not work')
                print('try to download resource')
                r = requests.get(self.file)
                self.original = ET.fromstring(r.text)
        try:
            self.tree = ET.parse(self.file)
        except Exception as e:
            print('could not parse tree')
            try:
                self.tree = ET.fromstring(self.file.encode('utf8'))
                print('read string worked')
            except Exception as e:
                print('read from string did not work')
                print('try to download resource')
                r = requests.get(self.file)
                self.tree = ET.fromstring(r.text)
        except Exception as e:
            print('parsing didnt work')
            self.parsed_file = "parsing didn't work"

    def return_byte_like_object(self):
        return ET.tostring(self.tree, encoding="utf-8")

    def return_string(self):
        return self.return_byte_like_object().decode('utf-8')

    def tei_stump(
        title="My Doc", publication_stmt="born digital", source_desc="created with help of teipy.TeiReader"
    ):
        """ returns a minmal valid TEI document as string """
        my_tei = """
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
          <teiHeader>
              <fileDesc>
                 <titleStmt>
                    <title>{}</title>
                 </titleStmt>
                 <publicationStmt>
                    <p>{}</p>
                 </publicationStmt>
                 <sourceDesc>
                    <p>{}</p>
                 </sourceDesc>
              </fileDesc>
          </teiHeader>
          <text>
              <body>
                 <p/>
              </body>
          </text>
        </TEI>
        """.format(title, publication_stmt, source_desc)
        return my_tei

    def tree_to_file(self, file=None):
        """saves current tree to file"""
        if file:
            pass
        else:
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
            file = "{}.xml".format(timestamp)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(self.return_string())
        return file

    def replace_child_nodes(self, xpath_to_parent, new_child_nodes):
        children_xpath = "{}/tei:*".format(xpath_to_parent)
        parent_node = self.tree.xpath(xpath_to_parent, namespaces=self.ns_tei)[0]
        for x in self.tree.xpath(children_xpath, namespaces=self.ns_tei):
            x.getparent().remove(x)
        for y in new_child_nodes:
            parent_node.append(y)

        return self.tree

    def get_author_nodes(self):

        """
        fetches all tei:author nodes form tei:titleStmt
        :return: a list of tei:author nodes
        """

        authors = self.tree.xpath(
            '//tei:titleStmt//tei:author[./tei:email]', namespaces=self.ns_tei
        )
        return authors

    def get_mail_addr(self):
        """
        :return: A tuple containg a tei:author node, the text node of its email child node\
        and a slugified version of it
        """
        for x in self.get_author_nodes():
            mail_addr = x.xpath(
                './tei:email/text()', namespaces=self.ns_tei
            )[0]
            slugged = slugify(mail_addr)
            print(slugged)
            yield (x, mail_addr, slugged)

    def add_refs(self):
        """
        :return: writes @ref attributes into tei:author nodes and yields the node
        """
        for x in self.get_mail_addr():
            x[0].attrib['ref'] = "#person__{}".format(x[2])
            yield x

    def make_slug(self, node):
        slug = slugify(node)
        return slug

    def fix_ids(self, node_name="tei:person", att_name="ana", substring_after="person__"):
        expr = "//{}".format(node_name)
        persons = self.tree.xpath(expr, namespaces=self.ns_tei)
        expr = './@{}'.format(att_name)
        for x in persons:
            old_id = x.xpath(expr, namespaces=self.ns_tei)[0]
            old_id = old_id.split(substring_after)[1]
            new_id = "{}{}".format(substring_after, slugify(old_id))
            x.attrib.pop("ana", None)
            x.attrib["{http://www.w3.org/XML/1998/namespace}id"] = new_id

    def addr_lines(self):
        return self.tree.xpath('//tei:addrLine', namespaces=self.ns_tei)

    def extract_md(self):
        xml_id = self.tree.xpath(
            './@xml:id', namespaces=self.ns_tei
        )
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
        try:
            md['xml_id'] = xml_id[0]
        except IndexError:
            md['xml_id'] = ""
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
        md['text_type'] = text_type
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


class ListOrg(TeiReader):
    """ a class to read an process tei-documents"""

    def get_orgs(self):
        items = self.tree.xpath(
            './/tei:listOrg//tei:org[./tei:idno[@type="GND"] and not(./tei:location)]',
            namespaces=self.ns_tei
        )
        for x in items:
            yield x

    def get_gnd(self, node):
        gnd = node.xpath('./tei:idno[@type="GND"]', namespaces=self.ns_tei)[0].text
        return gnd

    def add_coords(self):
        for x in self.get_orgs():
            gnd_url = self.get_gnd(x)
            result = get_place_of_business_info(gnd=gnd_url)
            if result is not None:
                location = ET.Element("{http://www.tei-c.org/ns/1.0}location")
                placename = ET.Element('placeName')
                placename.text = result['pref_name']
                placename.attrib['key'] = result['gnd_id']
                geo = ET.Element('geo')
                coords = result['coords']
                geo.text = "{} {}".format(coords[0], coords[1])
                location.append(placename)
                location.append(geo)
                x.append(location)
                yield x
            else:
                yield x
