// Runs the calculation block embedded in the HTML prototype and prints results as JSON.
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const PARAMS = JSON.parse(html.match(/const PARAMS = (\{.*?\});\n/s)[1]);
const calc = html.split('/*CALC*/')[1].split('/*ENDCALC*/')[0];
const f = new Function('PARAMS', calc + ';return {scenario,combine,actionImpact,projection,capacity,claimsOf};')(PARAMS);
const ex = PARAMS.worked_example, b = {S: ex.spend, roas: ex.roas, cpc: ex.cpc, cvr: ex.cvr};
const chosen = PARAMS.actions.filter(a => PARAMS.plan_ids.includes(a.id));
const CL = Object.fromEntries(Object.entries(PARAMS.claims).map(([k, v]) => [k, {re: new RegExp(v, 'i')}]));
console.log(JSON.stringify({
  profit: f.scenario(b).profit,
  planRoas: ['lo', 'mid', 'hi'].map(k => f.scenario(b, f.combine(chosen, k, PARAMS.damping)).roas),
  impacts: PARAMS.actions.map(a => f.actionImpact(b, a).mid),
  cap: f.capacity(f.scenario(b).clicks, ex.impression_share, 35, PARAMS.capacity_cpc_elasticity).extra,
  claims: f.claimsOf(PARAMS.example_ads.own.split('\n'), CL)
}));
