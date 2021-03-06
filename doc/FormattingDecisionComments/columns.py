import csv
import os
from io import StringIO

data = [
    ("OTP", "../../../otp"),
    ("kazoo", "../../../kazoo"),
    ("Inaka", "../../../../inaka"),
    ("MongooseIM", "../../../MongooseIM"),
    ("ejabberd", "../../../ejabberd"),
    ("WhatsApp", "~/local/whatsapp/server/erl"),
]

def genplot(name, path):
    out = os.popen(f"./columns.sh {path}").read()
    csvfile = StringIO(out)
    reader = csv.reader(csvfile, delimiter=',')
    rows = [row for row in reader]

    spaces = [int(row[0]) for row in rows]
    counts = [int(row[1]) for row in rows]
    total = sum(counts)
    percentages = [(c * 100) / total for c in counts]
    # filter out insignificant numbers, counts less than 10 and percentages less than 1
    filtered = [(s, p) for (s, c, p) in zip(spaces, counts, percentages) if p >= 1 and c >= 10]
    xs = [x for (x, y) in filtered]
    ys = [y for (x, y) in filtered]
    print("{")
    print(f"x: {xs},")
    print(f"y: {ys},")
    print("mode: 'markers',")
    print("type: 'scatter',")
    print(f"name: '{name}'")
    print("},")

print("""
<!-- generated by Makefile (python3 columns.py) -->

<html>
<head>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>

<body>
""")


print(f"""
<div id="myPlot"></div>
</div>
<script>
var data = [
""")

for (name, path) in data:
    genplot(name, path)

print(f"""
];

var layout =
""")
print("{")
print(f"""
title: 'Percentage of comments at column number',
""")
print("""
xaxis: {
    title: 'comment starts at column number'
},
yaxis: {
    title: 'percentage of comments'
}
};
""")
print(f"""

Plotly.newPlot('myPlot', data, layout);

</script>
""")

print("""
</body>
</html>
""")