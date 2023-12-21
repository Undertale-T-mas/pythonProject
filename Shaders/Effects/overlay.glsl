#version 330 core

in vec2 fragTexCoord;
uniform sampler2D sampler;
uniform sampler2D sampler_overlay;
uniform vec2 screen_size;

uniform float iTime;

uniform float iIntensity;
uniform float iWarn;
uniform vec2 iCamPos;

out vec4 fragColor;

#define e 2.71828

float activate(float v){
    v = min(v, 1);
    return 0.1 * pow(e, 3 * v) - 1 * pow(e, 6 * (v - 1));
}

void main()
{
    vec2 texCoord = fragTexCoord;
    fragColor = vec4((texture(sampler_overlay, (texCoord / 2.222 + iCamPos / screen_size)) * iIntensity + texture(sampler, texCoord)).xyz, 1.0);

    // sample the overlay sampler to get a noise. The overlay sampler is noise-like.
    float dir0 = atan(texCoord.y - 0.5, texCoord.x - 0.5);
    float dir = dir0 / (3.1415926 * 2) + 0.5;
    float dist = distance(vec2(0.5, 0.57 * 0.7), texCoord * vec2(1, 0.7));
    float it = dist * (1 + iWarn) - 0.81 + iWarn;
    float add = activate(it * 2.5) * (1 + iWarn);
    fragColor.r += add;
    add = add * add * add * 0.41;
    fragColor.g -= add;
    fragColor.b -= add;
}