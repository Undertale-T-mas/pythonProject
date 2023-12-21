#version 330 core

in vec2 texCoord;
uniform vec4 blend_color;
out vec4 fragColor;

void main()
{
    fragColor = blend_color;
}