#version 330 core

in vec2 fragTexCoord;
uniform vec2 screen_size;
uniform sampler2D sampler;

uniform vec2 iLightPos;
uniform float iIntensity;

out vec4 fragColor;

const int amount = 17;

vec4 col_local(vec2 pos_xy){
    return texture(sampler, pos_xy / screen_size);
}

void main()
{
    vec2 xy = fragTexCoord * screen_size;
    vec2 step = normalize(iLightPos - xy) * min(iIntensity, 12 * length((iLightPos - xy) / screen_size));
    vec2 cur = xy;
    vec3 resColor;
    for(int i = 0; i < amount; i++){
        resColor += col_local(cur).xyz;
        cur += step;
    }
    resColor /= amount;
/*
    vec4 original = col_local(xy);
    vec3 over = vec3(pow(original.x, 0.5), pow(original.y, 0.5), pow(original.z, 0.5));
    resColor = mix(original.xyz, over, resColor * 2.0);
    */
    fragColor = vec4(resColor, 1.0);
}