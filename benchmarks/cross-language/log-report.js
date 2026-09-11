// Idiomatic port of examples/log-report: validated TSV -> grouped, sorted TSV.
const fs = require("node:fs");

function integer(text) {
    text = text.trim();
    if (!/^[+-]?[0-9]+$/.test(text)) throw new Error("expected decimal integer");
    const value = Number(text);
    if (!Number.isSafeInteger(value)) throw new Error("integer outside exact Number range");
    return value;
}

function analyze(text) {
    const groups = new Map();
    for (const raw of text.split("\n")) {
        const line = raw.trim();
        if (!line || line.startsWith("#")) continue;
        const fields = line.split("\t");
        if (fields.length !== 4) throw new Error("expected four tab-separated fields");
        const route = fields[0].trim().split("?", 1)[0];
        if (!route.startsWith("/")) throw new Error("route must start with /");
        const status = integer(fields[1]);
        const latency = integer(fields[2]);
        const size = integer(fields[3]);
        if (status < 100 || status > 599 || latency < 0 || size < 0) {
            throw new Error("invalid status, latency, or byte count");
        }
        let stats = groups.get(route);
        if (stats === undefined) {
            stats = [0, 0, 0, 0, 0];
            groups.set(route, stats);
        }
        stats[0] += 1;
        stats[1] += Number(status >= 400);
        stats[2] += latency;
        stats[3] = Math.max(stats[3], latency);
        stats[4] += size;
    }
    return groups;
}

function report(groups) {
    const lines = ["route\trequests\terrors\tmean_ms\tmax_ms\tbytes"];
    for (const route of [...groups.keys()].sort()) {
        const [count, errors, total, maximum, size] = groups.get(route);
        lines.push(`${route}\t${count}\t${errors}\t${total / count}\t${maximum}\t${size}`);
    }
    return lines.join("\n") + "\n";
}

function checksum(groups) {
    let total = 0;
    for (const [route, [count, errors, sum, maximum, size]] of groups) {
        total += (Number(route.slice(route.lastIndexOf("/") + 1)) + 1) *
            (count * 3 + errors * 5 + sum * 7 + maximum * 11 + size * 13);
    }
    return total;
}

const text = fs.readFileSync(process.argv[2], "utf8");
const started = process.cpuUsage();
const groups = analyze(text);
const output = report(groups);
const elapsed = process.cpuUsage(started);
if (process.argv.length > 3) {
    process.stdout.write(output);
} else {
    console.log(checksum(groups));
    console.log(elapsed.user + elapsed.system);
}
