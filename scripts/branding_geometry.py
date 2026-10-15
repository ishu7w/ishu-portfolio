"""Replace only the identity inside the retained circular logo meshes."""
import json
import math
import struct
import zlib


def write_lab_mark(dist):
    """Rasterize a small code-defined IP emblem for the existing logo texture."""
    outer=[(205,72),(226,72),(235,81),(235,96),(226,105),(205,105)]
    inner=[(212,80),(223,80),(227,84),(227,93),(223,97),(212,97)]
    def inside(x,y,polygon):
        hit=False
        for i,(ax,ay) in enumerate(polygon):
            bx,by=polygon[(i+1)%len(polygon)]
            if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:
                hit=not hit
        return hit
    def white(x,y):
        return abs(math.hypot(x-200,y-100)-60)<2.5 or (168<x<191 and (72<y<79 or 121<y<128)) or (176<x<183 and 79<y<121) or (201<x<208 and 72<y<128) or (inside(x,y,outer) and not inside(x,y,inner))
    rows=[]
    for y in range(200):
        row=bytearray([0])
        for x in range(400):
            value=round(sum(white(x+dx,y+dy) for dx,dy in [(.25,.25),(.75,.25),(.25,.75),(.75,.75)])*255/4)
            row.extend([value,value,value])
        rows.append(bytes(row))
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',400,200,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b'')
    (dist/'content/portfolio/lab-mark.png').write_bytes(png)
    # A quiet background keeps the existing in-scene text legible.
    rows=[]
    for y in range(200):
        row=bytearray([0])
        for x in range(400):
            glow=math.exp(-((x-220)**2/24000+(y-100)**2/10000))
            ripple=(math.sin(x*.055+y*.04)+1)*.5
            row.extend([round(7+12*glow+2*ripple),round(11+23*glow+3*ripple),round(15+28*glow+4*ripple)])
        rows.append(bytes(row))
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',400,200,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b'')
    (dist/'content/portfolio/lab-map.png').write_bytes(png)


def make_monogram():
    mesh = {'position': [], 'normal': [], 'uv': []}
    depth = 0.0256114609

    def triangle(a, b, c):
        ab = [b[i] - a[i] for i in range(3)]
        ac = [c[i] - a[i] for i in range(3)]
        normal = [ab[1]*ac[2]-ab[2]*ac[1], ab[2]*ac[0]-ab[0]*ac[2], ab[0]*ac[1]-ab[1]*ac[0]]
        length = math.sqrt(sum(v*v for v in normal)) or 1
        normal = [n / length for n in normal]
        for point in [a, b, c]:
            mesh['position'].extend(point)
            mesh['normal'].extend(normal)
            mesh['uv'].extend([(point[0]+.36)/.72, (point[1]+.36)/.72])

    def extruded_quad(points):
        center=(sum(x for x,y in points)/len(points),sum(y for x,y in points)/len(points))
        inset=[(center[0]+(x-center[0])*.84,center[1]+(y-center[1])*.84) for x,y in points]
        front = [(x,y,depth) for x,y in inset]
        back = [(x,y,-depth) for x,y in inset]
        rim_front=[(x,y,depth-.004) for x,y in points]
        rim_back=[(x,y,-depth+.004) for x,y in points]
        for i in range(1,len(points)-1):
            triangle(front[0],front[i],front[i+1])
            triangle(back[0],back[i+1],back[i])
        for i in range(len(points)):
            n = (i+1)%len(points)
            for a,b,c,d in [(front[i],rim_front[i],rim_front[n],front[n]),(rim_front[i],rim_back[i],rim_back[n],rim_front[n]),(rim_back[i],back[i],back[n],rim_back[n])]:
                triangle(a,b,c)
                triangle(a,c,d)

    def rect(x0,y0,x1,y1):
        extruded_quad([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])

    # An architectural I and open-counter P with the original mesh thickness.
    rect(-.17,-.15,-.095,-.125)
    rect(-.148,-.125,-.117,.125)
    rect(-.17,.125,-.095,.15)
    rect(-.045,-.15,-.012,.15)
    outer = [(-.012,.15),(.10,.15),(.145,.11),(.145,.045),(.10,.005),(-.012,.005)]
    inner = [(-.012,.115),(.088,.115),(.11,.095),(.11,.062),(.088,.04),(-.012,.04)]
    for i in range(len(outer)):
        n=(i+1)%len(outer)
        # Reverse ordering keeps the visible face normal facing the camera.
        extruded_quad([outer[n],outer[i],inner[i],inner[n]])
    return mesh


def write_personal_geometry(dist):
    write_lab_mark(dist)
    personal = dist / 'assets/geometry/personal'
    personal.mkdir(parents=True, exist_ok=True)
    small = make_monogram()
    for source, target, cutoff, scale in [
        ('logo/AT_logo.json','ishu-logo.json',.28,1),
        ('home/logo.json','ishu-logo-large.json',2.05,2.682/.3595946034)
    ]:
        original = json.loads((dist/'assets/geometry'/source).read_text())
        result = {'position': [], 'normal': [], 'uv': []}
        p=original['position']
        for i in range(0,len(p),9):
            if all(math.hypot(p[k],p[k+1]) > cutoff for k in range(i,i+9,3)):
                result['position'].extend(p[i:i+9])
                result['normal'].extend(original['normal'][i:i+9])
                result['uv'].extend(original['uv'][i//3*2:(i//3+3)*2])
        result['position'].extend(v*scale for v in small['position'])
        result['normal'].extend(small['normal'])
        result['uv'].extend(small['uv'])
        (personal/target).write_text(json.dumps(result,separators=(',',':')))
