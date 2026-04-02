{%macro classify_earthquake_by_sig(magnitude) %}
    {% set sig = magnitude | float %}
    {% if sig >= 800 and sig >= 1000 %}
        {{ return("'Critical'") }}
    {% elif sig >= 600 and sig < 800 %}
        {{ return("'Emergency'") }}
    {% elif sig >= 400 and sig < 600 %}
        {{ return("'Warning'") }}
    {% elif sig >= 200 and sig < 400 %}
        {{ return("'Noticeable'") }}
    {%else %}
        {{ return("'Routine'") }}
    {% endif %}
    {% endmacro %}