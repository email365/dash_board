{%- extends 'full.tpl' -%}

{%-block input_group scoped-%}
{%- if 'jupyter:'  and cell.cell_type == 'code'-%}
{%- endif -%}
{%-endblock input_group -%}