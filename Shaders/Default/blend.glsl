#version 330 core

in vec2 fragTexCoord;
uniform vec4 blend_color;
uniform sampler2D sampler;

out vec4 fragColor;

void main()
{
    vec2 texCoord = fragTexCoord;
    vec4 textureColor = texture(sampler, texCoord);
    fragColor = textureColor * blend_color;
}