var celticColor = "#7becb2",
  italicColor = "#ecb27b",
  indoIranianColor = "#ec7bb6";

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const chart=Highcharts.chart('container', {

  chart: {
    type: 'networkgraph',
    marginTop: 80
  },

  title: {
    text: 'IOT Observation en temp reel'
  },

  subtitle: {
    text: 'Neighbour devices'
  },

  plotOptions: {
    networkgraph: {
      keys: ['from', 'to'],
      layoutAlgorithm: {
        enableSimulation: true,
        integration: 'verlet',
        linkLength: 100
      }
    }
  },
  linkFormat: '{point} \u2192 {point}',

  series: [{
    marker: {
      radius: 13,
    },
    dataLabels: {
      enabled: true,
      linkFormat: '',
      allowOverlap: true
    },
    data: [],
    nodes: []
  },{
    marker: {
      radius: 9,
    },
    dataLabels: {
      enabled: true,
      linkFormat: '',
      allowOverlap: true
    },
    data: [],
    nodes: []
  }]
});

const bleUid = (response) => {
  response.forEach(resp => {
    console.log(String(resp['manufact']), "", String(resp['services']))
    chart.series[1].addPoint([resp.addr, resp.uuid[0]+",RSSI:"+resp.rssi], true)
  });
  
}

fetch('http://127.0.0.1:5000/getpkt', { mode: 'cors', headers: { 'Access-Control-Allow-Origin':'*' } })
    .then((response) => response.body)
    .then((body) => {
        const reader = body.getReader();
        reader.read().then(function processText({ done, value }) {
            /* … */
            if(value) {
                let payload=Array.from(value).map(x=> String.fromCharCode(x)).join('').trim()
                payload=JSON.parse(payload)
                console.log(payload['payload'])
                if (payload.src == null) payload['src'] = "0x0000"
                if (payload.dst == null) payload['dst'] = "0x0001"
                if (payload.panid == null) payload['panid'] = "0x0002"
                chart.series[0].addPoint([[payload.src], [payload.dst], [payload.panid]], true)
                
                /*payloads=Array.from(payloads.match(/{[^}]+}/g))
                payloads.forEach(payload => {
                    payload=JSON.parse(payload)
                    console.log(payload['payload'])
                    if (payload.src == null) payload['src'] = "0x0000"
                    if (payload.dst == null) payload['dst'] = "0x0001"
                    //if (payload.panid == null) payload['panid'] = "0x0001"
                    chart.series[0].addPoint([[payload.panid, payload.src], [payload.panid, payload.dst]], true)
                });*/
            }
            //Promise.resolve(sleep(100));
            return reader.read().then(processText);
        })
        // …
    });

    