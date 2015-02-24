import sublime, sublime_plugin
import re

class PythonizeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    all_page = sublime.Region(0, self.view.size())

    line_regions = self.view.lines(all_page)
    line_texts = []
    for line in line_regions:
      line_texts.append(self.view.substr(line))

    longest = 90
    new_lines = []
    indent = 0

    for i in range(0, len(line_texts)):
      if len(line_texts[i].strip()) == 1:
        k = i
        while(len(line_texts[k].strip()) == 1):
            k = k - 1
        line_texts[k] += line_texts[i].lstrip().rstrip()

    for i in range(0, len(line_texts)):
      line_text = line_texts[i].lstrip().rstrip()

      ind = re.search("{|}|;", line_text).start()
      new_line =" " * indent + line_text[:ind]

      line_len = len(line_text) + indent

      if len(line_text) == 1:
        continue
      elif len(line_text) == 0:
        new_lines.append(line_text)
        continue

      last_part = line_text[ind:]
      gap = longest - (line_len - len(last_part))

      eol = " " * gap + last_part
      new_line += eol

      new_lines.append(new_line)

      if("{" in new_line):
        indent += 2
      elif("}" in new_line):
        indent -= 2 * last_part.count("}")

    self.view.replace(edit, all_page, "\n".join(new_lines))