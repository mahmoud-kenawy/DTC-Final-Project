{% macro classify_earthquake(magnitude) %}
  {% set mag = magnitude | float %}
  {% if mag >= 8 %}
        {{ return("'Great'") }}
  {% elif mag >= 7 and mag < 8 %}
        {{ return("'Major'") }}
  {% elif mag >= 6 and mag < 7 %}
        {{ return("'Strong'") }}
  {% elif mag >= 5 and mag < 6 %}
        {{ return("'Moderate'") }}
  {% elif mag >= 4 and mag < 5 %}
        {{ return("'Light'") }}
  {% elif mag >= 3 and mag < 4 %}
        {{ return("'Minor'") }}
  {% else %}
        {{ return("'Micro'") }}
  {% endif %}
{% endmacro %}
