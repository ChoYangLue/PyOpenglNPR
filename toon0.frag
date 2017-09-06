varying vec3 normal;
uniform sampler2D sampler;
varying vec3 P;//position vec
varying vec3 N;//normal vec

vec4 specular0;
vec4 ambient;
float microfacet;

// Beckman
float BechmannDistribution(float d, float m) {
    float d2 = d * d;
    float m2 = m * m;
    return exp((d2 - 1.0) / (d2 * m2)) / (m2 * d2 * d2);
}

float Fresnel(float c, float f0) {
    float sf = sqrt(f0);
    float n = (1.0 + sf) / (1.0 - sf);
    float g = sqrt(n * n + c * c - 1.0);
    float ga = (c * (g + c) - 1.0) * (c * (g + c) - 1.0);
    float gb = (c * (g - c) + 1.0) * (c * (g - c) + 1.0);
    return (g - c) * (g - c) / (2.0 * (g + c) + (g + c)) * (1.0 + ga / gb);
}

void main() {
    float intensity;
    vec4 color;
    vec3 n = normalize(normal);
    vec3 l = normalize(gl_LightSource[0].position).xyz;

	vec3 eyeV = normalize(-P.xyz);        //eyevec
	vec3  halfLE = normalize(l + eyeV);
	float specular  = pow(clamp(dot(N, halfLE), 0.0, 1.0), 70.0);

	vec3 h = normalize(l + eyeV);
	float hn = dot(h, n);
	float ln = dot(l, n);
	float lh = dot(l, h);
    float vn = dot(eyeV, n);

	//color = vec4(ln*col.x,ln*col.y,ln*col.z,1.0);

	specular0 = vec4(0.1, 0.1, 0.1, 1.0);
	microfacet = 0.1;
	//ambient = vec4(0.5, 0.5, 0.5, 1.0);
	// Cook-Torrance
	vec3 f = vec3(Fresnel(lh, specular0.x), Fresnel(lh, specular0.y), Fresnel(lh, specular0.z));
	float d = BechmannDistribution(hn, microfacet);
	float t = 2.0 * hn / dot(eyeV, h);
    float g = min(1.0, min(t * vn, t * ln));
    float m = 3.14159265 * vn * ln;
    vec3 spe = max(f * d * g / m, 0.0);
    //vec3 dif = max(ln, 0.0) * diffuse.xyz;
    //vec3 amb = ambient.xyz;


	//texture color
	vec4 texColor = texture2D(sampler, gl_TexCoord[0].st);

    // quantize to 5 steps (0, .25, .5, .75 and 1)
    intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;

if(intensity<=0.75){
intensity = 0.5;
}
else {
intensity = 1.0;
}

    color = vec4(1.0-intensity, 1.0-intensity, 1.0-intensity,intensity) -vec4(spe, 1.0);

    //gl_FragColor = color;
	gl_FragColor = texColor - color;
}