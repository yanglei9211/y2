from xml.dom import minidom


class XmlReader(object):
    def __init__(self):
        self.s = ""
        self.ts = ""

    def show_nodes(self, deep, node):
        # 树形展示节点
        nmp = node.attributes
        attr_str = "attrs: "
        if nmp:
            for i in range(nmp.length):
                # print nmp.item(i).name, nmp.item(i).value
                attr_str += "<%s: %s> /" % (nmp.item(i).name, nmp.item(i).value)

        print("\t" * deep, node.nodeName, node.nodeValue, attr_str)
        for node_child in node.childNodes:
            self.show_nodes(deep + 1, node_child)

    def do_str(self, node):
        res = ""
        for child in node.childNodes:
            # print child.nodeName, child.nodeValue
            # self.ts += "<p>%s</p>" % child.nodeValue
            res += child.nodeValue
        return res

    def do_para(self, node):
        res = ""
        for child in node.childNodes:
            if child.nodeName == 'str':
                ud_style = child.attributes.get('underline-style')
                ud_str = ud_style.nodeValue if ud_style else None
                em_style = child.attributes.get('em-style')
                em_str = em_style.nodeValue if em_style else None
                va_style = child.attributes.get('vertical-align')
                va_str = va_style.nodeValue if va_style else None
                content = self.do_str(child)
                if ud_str == 'solid':
                    content = "<span style=\"text-decoration:underline;\">%s</span>" % content
                if ud_str == 'wave':
                    content = "<span style=\"text-decoration:wavy underline;-webkit-text-decoration:wavy underline;\">%s</span>" % content
                if em_str == 'dot':
                    content = "<span style=\"text-emphasis: circle;text-emphasis-position:under;-webkit-text-emphasis:circle;-webkit-text-emphasis-position:under;\">%s</span>" % content
                if em_str == 'open':
                    content = "<span style=\"text-emphasis:open;-webkit-text-emphasis:open;\">%s</span>" % content
                if va_str == 'sub':
                    content = "<sub>%s</sub>" % content
                if va_str == 'super':
                    content = "<sup>%s</sub>" % content
                res += content

            elif child.nodeName == 'img':
                # at = child.attributes['src']
                # print at.nodeValue, at.nodeName
                # at2 = child.attributes['style']
                # print at2.nodeValue, at2.nodeName
                at_src = child.attributes.get('src')
                at_style = child.attributes.get('style')
                # print at_src.√, at_src.nodeName
                # print at_style.nodeValue, at_style.nodeName
                if at_src and at_style:
                    res += "<img src=\"%s\" style=\"%s\"/>" % (at_src.nodeValue, at_style.nodeValue)
                else:
                    raise Exception("error")
            elif child.nodeName == 'blank':
                # res += "______"
                res += "<span style=\"display:inline\"><mark type=\"blank\" style=\"display:none\"></mark>_____</span>"
            else:
                pass
                # print 'in para', child.nodeName
        res = "<p>%s</p>" % res
        return res

    def do_table(self, node):
        def do_table_node(node):
            ts = ""
            for child in node.childNodes:
                if child.nodeName == 'para':
                    # for sc in child.childNodes:
                    #     ts += "<p>%s</p>" % sc.nodeValue
                    ts += self.do_para(child)
                elif child.nodeName in ['tbody', 'tr', 'td']:
                    # print '=-=-=-=-=-=-=-='
                    # print child.nodeName, child.childNodes
                    r = do_table_node(child)
                    colspan = child.attributes.get('colspan')
                    rowspan = child.attributes.get('rowspan')

                    colspan_num = int(colspan.nodeValue) if colspan else None
                    rowspan_num = int(rowspan.nodeValue) if rowspan else None

                    # print child.nodeName, colspan_num, rowspan_num
                    if colspan_num and rowspan_num:
                        left = "<%s rowspan=%d colspan=%d>" % (
                            child.nodeName, colspan_num, rowspan_num)
                    elif colspan_num:
                        left = "<%s colspan=%d>" % (child.nodeName, colspan_num)
                    elif rowspan_num:
                        left = "<%s rowspan=%d>" % (child.nodeName, rowspan_num)
                    else:
                        left = "<%s>" % child.nodeName

                    ts += "%s%s</%s>" % (left, r, child.nodeName)
                    # for sc in child.childNodes:
                    #     tmp = do_table_node(sc)
                    #     ts += "<%s>%s</%s>" % (sc.nodeName, tmp, sc.nodeName)
                else:
                    ts = "<%s>todo</%s>" % (child.nodeName, child.nodeName)
            return ts
        res = do_table_node(node)
        res = "<table>%s</table>" % res
        return res

    def do_nodes(self, deep, node):
        if node.nodeName == 'para':
            self.ts += self.do_para(node)
        # elif node.nodeName == 'span':
        #     for child
        elif node.nodeName == 'doc':
            for child in node.childNodes:
                self.do_nodes(deep + 1, child)
        elif node.nodeName == '#text':
            self.ts += "%s" % node.nodeValue
        elif node.nodeName == 'table':
            self.ts += self.do_table(node)
        elif node.nodeName == 'str':
            # for child in node.childNodes:
            #     self.do_nodes(deep + 1, child)
            # todo 复制过来的,重构的时候再合并吧
            ud_style = node.attributes.get('underline-style')
            ud_str = ud_style.nodeValue if ud_style else None
            em_style = node.attributes.get('em-style')
            em_str = em_style.nodeValue if em_style else None
            va_style = node.attributes.get('vertical-align')
            va_str = va_style.nodeValue if va_style else None
            content = self.do_str(node)
            if ud_str == 'solid':
                content = "<span style=\"text-decoration:underline;\">%s</span>" % content
            if ud_str == 'wave':
                content = "<span style=\"text-decoration:wavy underline;-webkit-text-decoration:wavy underline;\">%s</span>" % content
            if em_str == 'dot':
                content = "<span style=\"text-emphasis: circle;text-emphasis-position:under;-webkit-text-emphasis:circle;-webkit-text-emphasis-position:under;\">%s</span>" % content
            if em_str == 'open':
                content = "<span style=\"text-emphasis:open;-webkit-text-emphasis:open;\">%s</span>" % content
            if va_str == 'sub':
                content = "<sub>%s</sub>" % content
            if va_str == 'super':
                content = "<sup>%s</sub>" % content
            self.ts += content
        else:
            self.ts += "<%s>todo<%s/>" % (node.nodeName, node.nodeName)


def do_text(s):
    if isinstance(s, int):
        return s

    if not s:
        return ""
    # print s
    # print s
    s = "<doc>%s</doc>" % s
    try:
        dom = minidom.parseString(s)
        root = dom.documentElement
        # res = root.toprettyxml
        # print res
        # show_nodes(0, root)
        reader = XmlReader()
        # reader.show_nodes(0, root)
        reader.do_nodes(0, root)
        return reader.ts
    except Exception as e:
        print(e)
        return s


# ori_str = '<str fake-selected=\"true\" font-family=\"SimSun\" xml_id=\"51\">选出下列每组单词中画线部分的读音与所给单词相同的一项。</str>\n<str xml_id=\"28\"> </str>[[nn]]<str xml_id=\"30\"> </str><str fake-selected=\"true\" font-family=\"Times New Roman\" underline-style=\"solid\" xml_id=\"31\">d</str><str fake-selected=\"true\" font-family=\"Times New Roman\" xml_id=\"32\">esk</str>'
# r = do_text(ori_str)
# print(r)

a =  "\u670d\u52a1\u5668\u5185\u90e8\\u9519\\u8bef\\uff0c\\u9ad8\\u8d28\\u91cf\\u9898\\u5e93\\u5de5\\u7a0b\\u5e08\u6b63\u5728\u5168\u529b\u62a2\u4fee"
print(a)
