import pypandoc


def md_to_html(stream):
    new_stream = stream
    res = re.findall(ur"([^- \n]+[- ]{4,}[-]+)", stream)
    for match in res:
        new_list = re.split(ur"[ ]+", match, maxsplit=1)
        new_list.reverse()
        new_str = "\n".join(new_list)
        new_stream = new_stream.replace(match, new_str)
    md = pypandoc.convert(new_stream, 'html', format='markdown')
    return md
