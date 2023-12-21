#version 330 core

layout (location = 0) in vec4 position;
layout (location = 1) in vec2 texCoord;

out vec2 fragTexCoord;

uniform int iflip;
uniform vec2 screen_size;

void main()
{
    vec2 posxy = vec2(position.x, position.y);
    vec2 posuv = posxy / screen_size * 2.0 - vec2(1.0, 1.0);
    gl_Position = vec4(posuv, position.z, 1.0);
    fragTexCoord = position.zw;
}
