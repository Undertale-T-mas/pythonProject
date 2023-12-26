#version 330 core

in vec2 fragTexCoord;
uniform vec2 screen_size;
uniform sampler2D sampler;

uniform float iSplit;

out vec4 fragColor;

void main()
{
    // do rgb split
    vec2 texCoord = fragTexCoord;
    vec4 tmp = texture(sampler, texCoord);
    fragColor.g = texture(sampler, texCoord + vec2(iSplit, 0)).g;
    fragColor.b = texture(sampler, texCoord - vec2(iSplit, 0)).b;
    fragColor.g = max(fragColor.g, texture(sampler, texCoord + vec2(iSplit * 0.5, 0)).g);
    fragColor.b = max(fragColor.b, texture(sampler, texCoord - vec2(iSplit * 0.5, 0)).b);
    fragColor.r = tmp.r;
    fragColor.a = tmp.a;
}