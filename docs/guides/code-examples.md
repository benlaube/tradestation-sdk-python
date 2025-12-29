# TradeStation API Code Examples from OpenAPI Spec

## Metadata

- **Status:** Active
- **Created:** 12-05-2025
- **Last Updated:** 12-05-2025 14:02:18 EST
- **Version:** 1.0
- **Description:** Centralized documentation of 190 code examples (Shell, Node.js, Python, C#, JSON) extracted from the TradeStation API v3 OpenAPI specification
- **Type:** Code Reference - Technical reference for developers implementing API integrations
- **Applicability:** When implementing API calls, understanding request/response formats, or learning API usage patterns
- **Dependencies:**
  - [`tradestation-api-v3-openapi.json`](../reference/tradestation-api-v3-openapi.json) - Source OpenAPI specification containing all examples
  - [`API_REFERENCE.md`](./API_REFERENCE.md) - Complete SDK API reference
  - [`SDK_USAGE_EXAMPLES.md`](./SDK_USAGE_EXAMPLES.md) - SDK-specific usage examples
- **How to Use:** Reference this document when implementing API calls in different languages, understanding request body formats, or comparing SDK implementation with raw API examples

---

**Total Examples Found:** 190

---

## C# Examples

### Example 1: GET /v2/data/symbols/suggest/{text}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v2/data/symbols/suggest/{text}"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 2: GET /v2/data/symbols/search/{criteria}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v2/data/symbols/search/{criteria}"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 3: GET /v2/stream/tickbars/{symbol}/{interval}/{barsBack}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v2/stream/tickbars/{symbol}/{interval}/{barsBack}"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 4: GET /v3/brokerage/accounts

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 5: GET /v3/brokerage/accounts/{accounts}/balances

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/balances"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 6: GET /v3/brokerage/accounts/{accounts}/bodbalances

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/bodbalances"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 7: GET /v3/brokerage/accounts/{accounts}/historicalorders

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders?since=2006-01-13"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 8: GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders/123456789,286179863?since=2006-01-13"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 9: GET /v3/brokerage/accounts/{accounts}/orders

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 10: GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders/123456789,286179863"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 11: GET /v3/brokerage/accounts/{accounts}/positions

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/positions"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 12: POST /v3/orderexecution/orderconfirm

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Post,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/orderconfirm"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
    Content = new StringContent("{\"AccountID\":\"123456782\",\"Symbol\":\"MSFT\",\"Quantity\":\"10\",\"OrderType\":\"Market\",\"TradeAction\":\"BUY\",\"TimeInForce\":{\"Duration\":\"DAY\"},\"Route\":\"Intelligent\"}")
    {
        Headers =
        {
            ContentType = new MediaTypeHeaderValue("application/json")
        }
    }
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 13: POST /v3/orderexecution/ordergroupconfirm

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Post,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/ordergroupconfirm"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
    Content = new StringContent("{\"Type\":\"OCO\",\"Orders\":[{\"AccountID\":\"123456782\",\"StopPrice\":\"337\",\"OrderType\":\"StopMarket\",\"Quantity\":\"10\",\"Route\":\"Intelligent\",\"Symbol\":\"MSFT\",\"TimeInForce\":{\"Duration\":\"GTC\"},\"TradeAction\":\"Buy\"},{\"AccountID\":\"123456782\",\"StopPrice\":\"333\",\"OrderType\":\"StopMarket\",\"Quantity\":\"10\",\"Route\":\"Intelligent\",\"Symbol\":\"MSFT\",\"TimeInForce\":{\"Duration\":\"GTC\"},\"TradeAction\":\"SellShort\"}]}")
    {
        Headers =
        {
            ContentType = new MediaTypeHeaderValue("application/json")
        }
    }
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 14: POST /v3/orderexecution/ordergroups

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Post,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/ordergroups"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
    Content = new StringContent("{\"Type\":\"OCO\",\"Orders\":[{\"AccountID\":\"123456782\",\"StopPrice\":\"337\",\"OrderType\":\"StopMarket\",\"Quantity\":\"10\",\"Route\":\"Intelligent\",\"Symbol\":\"MSFT\",\"TimeInForce\":{\"Duration\":\"GTC\"},\"TradeAction\":\"Buy\"},{\"AccountID\":\"123456782\",\"StopPrice\":\"333\",\"OrderType\":\"StopMarket\",\"Quantity\":\"10\",\"Route\":\"Intelligent\",\"Symbol\":\"MSFT\",\"TimeInForce\":{\"Duration\":\"GTC\"},\"TradeAction\":\"SellShort\"}]}")
    {
        Headers =
        {
            ContentType = new MediaTypeHeaderValue("application/json")
        }
    }
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 15: POST /v3/orderexecution/orders

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Post,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/orders"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
    Content = new StringContent("{\"AccountID\":\"123456782\",\"Symbol\":\"MSFT\",\"Quantity\":\"10\",\"OrderType\":\"Market\",\"TradeAction\":\"BUY\",\"TimeInForce\":{\"Duration\":\"DAY\"},\"Route\":\"Intelligent\"}")
    {
        Headers =
        {
            ContentType = new MediaTypeHeaderValue("application/json")
        }
    }
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 16: PUT /v3/orderexecution/orders/{orderID}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Put,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/orders/123456789"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
    Content = new StringContent("{\"Quantity\":\"10\",\"LimitPrice\":\"132.52\"}")
    {
        Headers =
        {
            ContentType = new MediaTypeHeaderValue("application/json")
        }
    }
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 17: DELETE /v3/orderexecution/orders/{orderID}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Delete,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/orders/123456789"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 18: GET /v3/marketdata/barcharts/{symbol}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/barcharts/MSFT"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 19: GET /v3/marketdata/stream/barcharts/{symbol}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/stream/barcharts/MSFT"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 20: GET /v3/marketdata/symbollists/cryptopairs/symbolnames

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/symbollists/cryptopairs/symbolnames"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 21: GET /v3/marketdata/symbols/{symbols}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/symbols/MSFT,BTCUSD"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 22: GET /v3/orderexecution/activationtriggers

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/activationtriggers"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 23: GET /v3/orderexecution/routes

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/orderexecution/routes"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 24: GET /v3/marketdata/options/expirations/{underlying}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/options/expirations/AAPL"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 25: POST /v3/marketdata/options/riskreward

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Post,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/options/riskreward"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
    Content = new StringContent("{\"SpreadPrice\":0.1,\"Legs\":[{\"Symbol\":\"string\",\"Quantity\":0,\"TradeAction\":\"BUY\"}]}")
    {
        Headers =
        {
            ContentType = new MediaTypeHeaderValue("application/json")
        }
    }
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 26: GET /v3/marketdata/options/spreadtypes

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/options/spreadtypes"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 27: GET /v3/marketdata/options/strikes/{underlying}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/options/strikes/AAPL"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 28: GET /v3/marketdata/stream/options/chains/{underlying}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/stream/options/chains/AAPL"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 29: GET /v3/marketdata/stream/options/quotes

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/stream/options/quotes?legs%5B0%5D.Symbol=MSFT%20220916C305"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 30: GET /v3/marketdata/quotes/{symbols}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/quotes/MSFT,BTCUSD"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request))
{
    response.EnsureSuccessStatusCode();
    var body = await response.Content.ReadAsStringAsync();
    Console.WriteLine(body);
}
```

---

### Example 31: GET /v3/marketdata/stream/quotes/{symbols}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/stream/quotes/MSFT,BTCUSD"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 32: GET /v3/marketdata/stream/marketdepth/quotes/{symbol}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/stream/marketdepth/quotes/MSFT"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 33: GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/marketdata/stream/marketdepth/aggregates/MSFT"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 34: GET /v3/brokerage/stream/accounts/{accounts}/orders

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 35: GET /v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders/812767578,812941051"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

### Example 36: GET /v3/brokerage/stream/accounts/{accounts}/positions

```c#
var client = new HttpClient();
var request = new HttpRequestMessage
{
    Method = HttpMethod.Get,
    RequestUri = new Uri("https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/positions"),
    Headers =
    {
        { "Authorization", "Bearer TOKEN" },
    },
};
using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead))
{
    response.EnsureSuccessStatusCode();
    using (var stream = await response.Content.ReadAsStreamAsync())
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                Console.WriteLine(line);
            }
        }
    }
}
```

---

## JSON Examples

### Example 1: POST /v3/orderexecution/orderconfirm

**Example Name:** Market Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "Market",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "DAY"
  },
  "Route": "Intelligent"
}
```

---

### Example 2: POST /v3/orderexecution/orderconfirm

**Example Name:** Limit Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "Limit",
  "TradeAction": "BUY",
  "LimitPrice": "132.52",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Route": "Intelligent"
}
```

---

### Example 3: POST /v3/orderexecution/orderconfirm

**Example Name:** Stop Market Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "StopMarket",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Route": "Intelligent",
  "StopPrice": "215.00"
}
```

---

### Example 4: POST /v3/orderexecution/orderconfirm

**Example Name:** Stop Limit Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "StopLimit",
  "TradeAction": "SELL",
  "StopPrice": "215.00",
  "LimitPrice": "200.00",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Route": "Intelligent"
}
```

---

### Example 5: POST /v3/orderexecution/orderconfirm

**Example Name:** Single Option Order

```json
{
  "AccountId": "123456782",
  "Symbol": "MSFT",
  "Quantity": "1",
  "OrderType": "Market",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "DAY"
  },
  "Route": "Intelligent",
  "Legs": [
    {
      "Symbol": "MSFT 201120P110",
      "Quantity": "1",
      "TradeAction": "BuyToOpen"
    }
  ]
}
```

---

### Example 6: POST /v3/orderexecution/orderconfirm

**Example Name:** Covered/Married Stock

```json
{
  "AccountID": "123456782",
  "OrderType": "Limit",
  "LimitPrice": "350",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Legs": [
    {
      "Symbol": "MSFT",
      "TradeAction": "BuyToOpen",
      "Quantity": 100
    },
    {
      "Symbol": "MSFT 251219P300",
      "TradeAction": "BuyToOpen",
      "Quantity": 1
    }
  ]
}
```

---

### Example 7: POST /v3/orderexecution/orderconfirm

**Example Name:** Vertical Option Spread

```json
{
  "AccountID": "123456782",
  "OrderType": "Limit",
  "LimitPrice": "1",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Legs": [
    {
      "Symbol": "SPY 251219C320",
      "TradeAction": "SELLTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219C300",
      "TradeAction": "BUYTOOPEN",
      "Quantity": "1"
    }
  ]
}
```

---

### Example 8: POST /v3/orderexecution/orderconfirm

**Example Name:** Iron Condor (Sell Entry)

```json
{
  "AccountID": "123456782",
  "OrderType": "Limit",
  "LimitPrice": "-20",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Legs": [
    {
      "Symbol": "SPY 251219C420",
      "TradeAction": "SELLTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219C430",
      "TradeAction": "BUYTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219P380",
      "TradeAction": "SELLTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219P370",
      "TradeAction": "BUYTOOPEN",
      "Quantity": "1"
    }
  ]
}
```

---

### Example 9: POST /v3/orderexecution/orderconfirm

**Example Name:** Order Sends Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "Limit",
  "TradeAction": "BUY",
  "LimitPrice": "130.00",
  "Route": "Intelligent",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "OSOs": [
    {
      "Type": "Normal",
      "Orders": [
        {
          "AccountID": "123456782",
          "Symbol": "AAPL",
          "Quantity": "5",
          "OrderType": "Limit",
          "TradeAction": "BUY",
          "LimitPrice": "50.00",
          "Route": "Intelligent",
          "TimeInForce": {
            "Duration": "GTC"
          }
        },
        {
          "AccountID": "123456782",
          "Symbol": "MSFT",
          "Quantity": "10",
          "OrderType": "StopMarket",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "AdvancedOptions": {
            "TrailingStop": {
              "Percent": "5.0"
            }
          }
        }
      ]
    }
  ]
}
```

---

### Example 10: POST /v3/orderexecution/orderconfirm

**Example Name:** Limit Entry with Amount Trail Stop

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Quantity": "1",
  "OrderType": "Limit",
  "Symbol": "MSFT",
  "TradeAction": "BUY",
  "Route": "Intelligent",
  "LimitPrice": "330",
  "OSOs": [
    {
      "Type": "NORMAL",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "1",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "AdvancedOptions": {
            "TrailingStop": {
              "Amount": "10"
            }
          }
        }
      ]
    }
  ]
}
```

---

### Example 11: POST /v3/orderexecution/orderconfirm

**Example Name:** Long Entry with Exit Bracket - 1 Limit & 1 Stop

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "1",
  "OrderType": "Limit",
  "LimitPrice": "225.00",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "IOC"
  },
  "Route": "Intelligent",
  "OSOs": [
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "Symbol": "MSFT",
          "Quantity": "1",
          "OrderType": "Limit",
          "LimitPrice": "300.00",
          "TradeAction": "SELL",
          "TimeInForce": {
            "Duration": "DAY"
          },
          "Route": "Intelligent"
        },
        {
          "AccountID": "123456782",
          "Symbol": "MSFT",
          "Quantity": "1",
          "OrderType": "StopMarket",
          "TradeAction": "SELL",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Route": "Intelligent",
          "AdvancedOptions": {
            "TrailingStop": {
              "Percent": "5.0"
            }
          }
        }
      ]
    }
  ]
}
```

---

### Example 12: POST /v3/orderexecution/orderconfirm

**Example Name:** Buy Limit Entry with Multiple Brackets

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Quantity": "10",
  "OrderType": "Limit",
  "Symbol": "MSFT",
  "TradeAction": "BUY",
  "Route": "Intelligent",
  "LimitPrice": "330",
  "OSOs": [
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "StopPrice": "325"
        },
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "Limit",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "LimitPrice": "335"
        }
      ]
    },
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "StopPrice": "325"
        },
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "Limit",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "LimitPrice": "340"
        }
      ]
    }
  ]
}
```

---

### Example 13: POST /v3/orderexecution/orderconfirm

**Example Name:** Sell Short Stocks with Bracket - 1 Limit & 1 Stop

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Quantity": "1",
  "OrderType": "Limit",
  "Symbol": "MSFT",
  "TradeAction": "SellShort",
  "Route": "Intelligent",
  "LimitPrice": "360",
  "OSOs": [
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "1",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "BuyToCover",
          "Route": "Intelligent",
          "StopPrice": "370"
        },
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "1",
          "OrderType": "Limit",
          "Symbol": "MSFT",
          "TradeAction": "BuyToCover",
          "Route": "Intelligent",
          "LimitPrice": "350"
        }
      ]
    }
  ]
}
```

---

### Example 14: POST /v3/orderexecution/orderconfirm

**Example Name:** Market Activation Rules

```json
{
  "Symbol": "MSFT",
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "OrderType": "Market",
  "Quantity": "10",
  "Route": "Intelligent",
  "TradeAction": "BUY",
  "AdvancedOptions": {
    "MarketActivationRules": [
      {
        "RuleType": "Price",
        "Symbol": "EDZ22",
        "Predicate": "Gt",
        "TriggerKey": "STTN",
        "Price": "10000.01"
      }
    ],
    "TimeActivationRules": [
      {
        "TimeUtc": "0001-01-01T23:59:59.000Z"
      }
    ]
  }
}
```

---

### Example 15: POST /v3/orderexecution/orderconfirm

**Example Name:** Sell Limit Order - Time Activation

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "OrderType": "Limit",
  "LimitPrice": "300",
  "Quantity": "1",
  "Route": "Intelligent",
  "Symbol": "MSFT",
  "TradeAction": "Sell",
  "AdvancedOptions": {
    "TimeActivationRules": [
      {
        "TimeUtc": "0001-01-01T18:50:00.000Z"
      }
    ]
  }
}
```

---

### Example 16: POST /v3/orderexecution/orderconfirm

**Example Name:** Reverse Long Position (Stocks)

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "Day"
  },
  "Quantity": "100",
  "OrderType": "Market",
  "Symbol": "MSFT",
  "TradeAction": "SELL",
  "Route": "Intelligent",
  "OSOs": [
    {
      "Type": "NORMAL",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "Day"
          },
          "Quantity": "100",
          "OrderType": "Market",
          "Symbol": "MSFT",
          "TradeAction": "SELLSHORT",
          "Route": "Intelligent"
        }
      ]
    }
  ]
}
```

---

### Example 17: POST /v3/orderexecution/ordergroupconfirm

**Example Name:** OCO Breakout Entry (Stocks)

```json
{
  "Type": "OCO",
  "Orders": [
    {
      "AccountID": "123456782",
      "StopPrice": "337",
      "OrderType": "StopMarket",
      "Quantity": "10",
      "Route": "Intelligent",
      "Symbol": "MSFT",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "StopPrice": "333",
      "OrderType": "StopMarket",
      "Quantity": "10",
      "Route": "Intelligent",
      "Symbol": "MSFT",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "TradeAction": "SellShort"
    }
  ]
}
```

---

### Example 18: POST /v3/orderexecution/ordergroupconfirm

**Example Name:** Exit Bracket - 1 Limit & 1 Stop

```json
{
  "Type": "BRK",
  "Orders": [
    {
      "AccountID": "123456782",
      "Symbol": "MSFT",
      "Quantity": "10",
      "OrderType": "Limit",
      "TradeAction": "SELL",
      "LimitPrice": "230.00",
      "Route": "Intelligent",
      "TimeInForce": {
        "Duration": "GTC"
      }
    },
    {
      "AccountID": "123456782",
      "Symbol": "MSFT",
      "Quantity": "10",
      "OrderType": "StopMarket",
      "TradeAction": "SELL",
      "Route": "Intelligent",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "AdvancedOptions": {
        "TrailingStop": {
          "Percent": "5.0"
        }
      }
    }
  ]
}
```

---

### Example 19: POST /v3/orderexecution/ordergroupconfirm

**Example Name:** Grouped Normal Order (NORMAL)

```json
{
  "Type": "NORMAL",
  "Orders": [
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "AMZN",
      "OrderType": "Limit",
      "LimitPrice": "1600.00",
      "Quantity": "2",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "AAPL",
      "OrderType": "Limit",
      "LimitPrice": "60.00",
      "Quantity": "50",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "MSFT",
      "OrderType": "Limit",
      "LimitPrice": "150.00",
      "Quantity": "10",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "GE",
      "OrderType": "Limit",
      "LimitPrice": "6.00",
      "Quantity": "100",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "MMM",
      "OrderType": "Limit",
      "LimitPrice": "120.00",
      "Quantity": "10",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "FB",
      "OrderType": "Limit",
      "LimitPrice": "150.00",
      "Quantity": "2",
      "TradeAction": "Buy"
    }
  ]
}
```

---

### Example 20: POST /v3/orderexecution/ordergroupconfirm

**Example Name:** Market Activation Rules

```json
{
  "Type": "OCO",
  "Orders": [
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Quantity": "10",
      "OrderType": "Limit",
      "LimitPrice": "230.00",
      "Symbol": "MSFT",
      "TradeAction": "SELL",
      "Route": "Intelligent",
      "AdvancedOptions": {
        "MarketActivationRules": [
          {
            "RuleType": "Price",
            "Symbol": "EDZ22",
            "Predicate": "Lt",
            "TriggerKey": "STTN",
            "Price": "10000.01"
          }
        ],
        "TimeActivationRules": [
          {
            "TimeUtc": "0001-01-01T23:59:59.000Z"
          }
        ]
      }
    },
    {
      "AccountID": "31002504",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Quantity": "10",
      "OrderType": "StopMarket",
      "Symbol": "MSFT",
      "TradeAction": "SELL",
      "Route": "Intelligent",
      "AdvancedOptions": {
        "MarketActivationRules": [
          {
            "RuleType": "Price",
            "Symbol": "EDZ22",
            "Predicate": "Lt",
            "TriggerKey": "STTN",
            "Price": "10000.01"
          },
          {
            "RuleType": "Price",
            "Symbol": "EDZ22",
            "Predicate": "Lt",
            "TriggerKey": "STTN",
            "Price": "999999.99",
            "LogicOperator": "Or"
          }
        ],
        "TimeActivationRules": [
          {
            "TimeUtc": "0001-01-01T23:59:59.000Z"
          }
        ],
        "AdvancedOptions": {
          "TrailingStop": {
            "Percent": "5.0"
          }
        }
      }
    }
  ]
}
```

---

### Example 21: POST /v3/orderexecution/ordergroups

**Example Name:** OCO Breakout Entry (Stocks)

```json
{
  "Type": "OCO",
  "Orders": [
    {
      "AccountID": "123456782",
      "StopPrice": "337",
      "OrderType": "StopMarket",
      "Quantity": "10",
      "Route": "Intelligent",
      "Symbol": "MSFT",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "StopPrice": "333",
      "OrderType": "StopMarket",
      "Quantity": "10",
      "Route": "Intelligent",
      "Symbol": "MSFT",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "TradeAction": "SellShort"
    }
  ]
}
```

---

### Example 22: POST /v3/orderexecution/ordergroups

**Example Name:** Exit Bracket - 1 Limit & 1 Stop

```json
{
  "Type": "BRK",
  "Orders": [
    {
      "AccountID": "123456782",
      "Symbol": "MSFT",
      "Quantity": "10",
      "OrderType": "Limit",
      "TradeAction": "SELL",
      "LimitPrice": "230.00",
      "Route": "Intelligent",
      "TimeInForce": {
        "Duration": "GTC"
      }
    },
    {
      "AccountID": "123456782",
      "Symbol": "MSFT",
      "Quantity": "10",
      "OrderType": "StopMarket",
      "TradeAction": "SELL",
      "Route": "Intelligent",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "AdvancedOptions": {
        "TrailingStop": {
          "Percent": "5.0"
        }
      }
    }
  ]
}
```

---

### Example 23: POST /v3/orderexecution/ordergroups

**Example Name:** Grouped Normal Order (NORMAL)

```json
{
  "Type": "NORMAL",
  "Orders": [
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "AMZN",
      "OrderType": "Limit",
      "LimitPrice": "1600.00",
      "Quantity": "2",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "AAPL",
      "OrderType": "Limit",
      "LimitPrice": "60.00",
      "Quantity": "50",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "MSFT",
      "OrderType": "Limit",
      "LimitPrice": "150.00",
      "Quantity": "10",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "GE",
      "OrderType": "Limit",
      "LimitPrice": "6.00",
      "Quantity": "100",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "MMM",
      "OrderType": "Limit",
      "LimitPrice": "120.00",
      "Quantity": "10",
      "TradeAction": "Buy"
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Symbol": "FB",
      "OrderType": "Limit",
      "LimitPrice": "150.00",
      "Quantity": "2",
      "TradeAction": "Buy"
    }
  ]
}
```

---

### Example 24: POST /v3/orderexecution/ordergroups

**Example Name:** Market Activation Rules

```json
{
  "Type": "OCO",
  "Orders": [
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Quantity": "10",
      "OrderType": "Limit",
      "LimitPrice": "230.00",
      "Symbol": "MSFT",
      "TradeAction": "SELL",
      "Route": "Intelligent",
      "AdvancedOptions": {
        "MarketActivationRules": [
          {
            "RuleType": "Price",
            "Symbol": "EDZ22",
            "Predicate": "Lt",
            "TriggerKey": "STTN",
            "Price": "10000.01"
          }
        ],
        "TimeActivationRules": [
          {
            "TimeUtc": "0001-01-01T23:59:59.000Z"
          }
        ]
      }
    },
    {
      "AccountID": "31002504",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Quantity": "10",
      "OrderType": "StopMarket",
      "Symbol": "MSFT",
      "TradeAction": "SELL",
      "Route": "Intelligent",
      "AdvancedOptions": {
        "MarketActivationRules": [
          {
            "RuleType": "Price",
            "Symbol": "EDZ22",
            "Predicate": "Lt",
            "TriggerKey": "STTN",
            "Price": "10000.01"
          },
          {
            "RuleType": "Price",
            "Symbol": "EDZ22",
            "Predicate": "Lt",
            "TriggerKey": "STTN",
            "Price": "999999.99",
            "LogicOperator": "Or"
          }
        ],
        "TimeActivationRules": [
          {
            "TimeUtc": "0001-01-01T23:59:59.000Z"
          }
        ],
        "AdvancedOptions": {
          "TrailingStop": {
            "Percent": "5.0"
          }
        }
      }
    },
    {
      "AccountID": "123456782",
      "TimeInForce": {
        "Duration": "GTC"
      },
      "Quantity": "10",
      "OrderType": "Limit",
      "LimitPrice": "50000.00",
      "Symbol": "TSLA",
      "TradeAction": "BUY",
      "Route": "Intelligent",
      "AdvancedOptions": {
        "MarketActivationRules": [
          {
            "RuleType": "Price",
            "Symbol": "EDZ22",
            "Predicate": "Lt",
            "TriggerKey": "STTN",
            "Price": "10000.01"
          }
        ],
        "TimeActivationRules": [
          {
            "TimeUtc": "0001-01-01T23:59:59.000Z"
          }
        ]
      }
    }
  ]
}
```

---

### Example 25: POST /v3/orderexecution/orders

**Example Name:** Market Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "Market",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "DAY"
  },
  "Route": "Intelligent"
}
```

---

### Example 26: POST /v3/orderexecution/orders

**Example Name:** Limit Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "Limit",
  "TradeAction": "BUY",
  "LimitPrice": "132.52",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Route": "Intelligent"
}
```

---

### Example 27: POST /v3/orderexecution/orders

**Example Name:** Stop Market Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "StopMarket",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Route": "Intelligent",
  "StopPrice": "215.00"
}
```

---

### Example 28: POST /v3/orderexecution/orders

**Example Name:** Stop Limit Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "StopLimit",
  "TradeAction": "SELL",
  "StopPrice": "215.00",
  "LimitPrice": "200.00",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Route": "Intelligent"
}
```

---

### Example 29: POST /v3/orderexecution/orders

**Example Name:** Single Option Order

```json
{
  "AccountId": "123456782",
  "Symbol": "MSFT",
  "Quantity": "1",
  "OrderType": "Market",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "DAY"
  },
  "Route": "Intelligent",
  "Legs": [
    {
      "Symbol": "MSFT 201120P110",
      "Quantity": "1",
      "TradeAction": "BuyToOpen"
    }
  ]
}
```

---

### Example 30: POST /v3/orderexecution/orders

**Example Name:** Covered/Married Stock

```json
{
  "AccountID": "123456782",
  "OrderType": "Limit",
  "LimitPrice": "350",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Legs": [
    {
      "Symbol": "MSFT",
      "TradeAction": "BuyToOpen",
      "Quantity": 100
    },
    {
      "Symbol": "MSFT 251219P300",
      "TradeAction": "BuyToOpen",
      "Quantity": 1
    }
  ]
}
```

---

### Example 31: POST /v3/orderexecution/orders

**Example Name:** Vertical Option Spread

```json
{
  "AccountID": "123456782",
  "OrderType": "Limit",
  "LimitPrice": "1",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Legs": [
    {
      "Symbol": "SPY 251219C320",
      "TradeAction": "SELLTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219C300",
      "TradeAction": "BUYTOOPEN",
      "Quantity": "1"
    }
  ]
}
```

---

### Example 32: POST /v3/orderexecution/orders

**Example Name:** Iron Condor (Sell Entry)

```json
{
  "AccountID": "123456782",
  "OrderType": "Limit",
  "LimitPrice": "-20",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Legs": [
    {
      "Symbol": "SPY 251219C420",
      "TradeAction": "SELLTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219C430",
      "TradeAction": "BUYTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219P380",
      "TradeAction": "SELLTOOPEN",
      "Quantity": "1"
    },
    {
      "Symbol": "SPY 251219P370",
      "TradeAction": "BUYTOOPEN",
      "Quantity": "1"
    }
  ]
}
```

---

### Example 33: POST /v3/orderexecution/orders

**Example Name:** Order Sends Order

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "10",
  "OrderType": "Limit",
  "TradeAction": "BUY",
  "LimitPrice": "130.00",
  "Route": "Intelligent",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "OSOs": [
    {
      "Type": "Normal",
      "Orders": [
        {
          "AccountID": "123456782",
          "Symbol": "AAPL",
          "Quantity": "5",
          "OrderType": "Limit",
          "TradeAction": "BUY",
          "LimitPrice": "50.00",
          "Route": "Intelligent",
          "TimeInForce": {
            "Duration": "GTC"
          }
        },
        {
          "AccountID": "123456782",
          "Symbol": "MSFT",
          "Quantity": "10",
          "OrderType": "StopMarket",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "AdvancedOptions": {
            "TrailingStop": {
              "Percent": "5.0"
            }
          }
        }
      ]
    }
  ]
}
```

---

### Example 34: POST /v3/orderexecution/orders

**Example Name:** Limit Entry with Amount Trail Stop

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Quantity": "1",
  "OrderType": "Limit",
  "Symbol": "MSFT",
  "TradeAction": "BUY",
  "Route": "Intelligent",
  "LimitPrice": "330",
  "OSOs": [
    {
      "Type": "NORMAL",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "1",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "AdvancedOptions": {
            "TrailingStop": {
              "Amount": "10"
            }
          }
        }
      ]
    }
  ]
}
```

---

### Example 35: POST /v3/orderexecution/orders

**Example Name:** Long Entry with Exit Bracket - 1 Limit & 1 Stop

```json
{
  "AccountID": "123456782",
  "Symbol": "MSFT",
  "Quantity": "1",
  "OrderType": "Limit",
  "LimitPrice": "225.00",
  "TradeAction": "BUY",
  "TimeInForce": {
    "Duration": "IOC"
  },
  "Route": "Intelligent",
  "OSOs": [
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "Symbol": "MSFT",
          "Quantity": "1",
          "OrderType": "Limit",
          "LimitPrice": "300.00",
          "TradeAction": "SELL",
          "TimeInForce": {
            "Duration": "DAY"
          },
          "Route": "Intelligent"
        },
        {
          "AccountID": "123456782",
          "Symbol": "MSFT",
          "Quantity": "1",
          "OrderType": "StopMarket",
          "TradeAction": "SELL",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Route": "Intelligent",
          "AdvancedOptions": {
            "TrailingStop": {
              "Percent": "5.0"
            }
          }
        }
      ]
    }
  ]
}
```

---

### Example 36: POST /v3/orderexecution/orders

**Example Name:** Buy Limit Entry with Multiple Brackets

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Quantity": "10",
  "OrderType": "Limit",
  "Symbol": "MSFT",
  "TradeAction": "BUY",
  "Route": "Intelligent",
  "LimitPrice": "330",
  "OSOs": [
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "StopPrice": "325"
        },
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "Limit",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "LimitPrice": "335"
        }
      ]
    },
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "StopPrice": "325"
        },
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "5",
          "OrderType": "Limit",
          "Symbol": "MSFT",
          "TradeAction": "SELL",
          "Route": "Intelligent",
          "LimitPrice": "340"
        }
      ]
    }
  ]
}
```

---

### Example 37: POST /v3/orderexecution/orders

**Example Name:** Sell Short Stocks with Bracket - 1 Limit & 1 Stop

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "Quantity": "1",
  "OrderType": "Limit",
  "Symbol": "MSFT",
  "TradeAction": "SellShort",
  "Route": "Intelligent",
  "LimitPrice": "360",
  "OSOs": [
    {
      "Type": "BRK",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "1",
          "OrderType": "StopMarket",
          "Symbol": "MSFT",
          "TradeAction": "BuyToCover",
          "Route": "Intelligent",
          "StopPrice": "370"
        },
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "GTC"
          },
          "Quantity": "1",
          "OrderType": "Limit",
          "Symbol": "MSFT",
          "TradeAction": "BuyToCover",
          "Route": "Intelligent",
          "LimitPrice": "350"
        }
      ]
    }
  ]
}
```

---

### Example 38: POST /v3/orderexecution/orders

**Example Name:** Market Activation Rules

```json
{
  "Symbol": "MSFT",
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "OrderType": "Market",
  "Quantity": "10",
  "Route": "Intelligent",
  "TradeAction": "BUY",
  "AdvancedOptions": {
    "MarketActivationRules": [
      {
        "RuleType": "Price",
        "Symbol": "EDZ22",
        "Predicate": "Gt",
        "TriggerKey": "STTN",
        "Price": "10000.01"
      }
    ],
    "TimeActivationRules": [
      {
        "TimeUtc": "0001-01-01T23:59:59.000Z"
      }
    ]
  }
}
```

---

### Example 39: POST /v3/orderexecution/orders

**Example Name:** Sell Limit Order - Time Activation

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "GTC"
  },
  "OrderType": "Limit",
  "LimitPrice": "300",
  "Quantity": "1",
  "Route": "Intelligent",
  "Symbol": "MSFT",
  "TradeAction": "Sell",
  "AdvancedOptions": {
    "TimeActivationRules": [
      {
        "TimeUtc": "0001-01-01T18:50:00.000Z"
      }
    ]
  }
}
```

---

### Example 40: POST /v3/orderexecution/orders

**Example Name:** Reverse Long Position (Stocks)

```json
{
  "AccountID": "123456782",
  "TimeInForce": {
    "Duration": "Day"
  },
  "Quantity": "100",
  "OrderType": "Market",
  "Symbol": "MSFT",
  "TradeAction": "SELL",
  "Route": "Intelligent",
  "OSOs": [
    {
      "Type": "NORMAL",
      "Orders": [
        {
          "AccountID": "123456782",
          "TimeInForce": {
            "Duration": "Day"
          },
          "Quantity": "100",
          "OrderType": "Market",
          "Symbol": "MSFT",
          "TradeAction": "SELLSHORT",
          "Route": "Intelligent"
        }
      ]
    }
  ]
}
```

---

### Example 41: PUT /v3/orderexecution/orders/{orderID}

**Example Name:** Limit Order

```json
{
  "Quantity": "10",
  "LimitPrice": "132.52"
}
```

---

### Example 42: PUT /v3/orderexecution/orders/{orderID}

**Example Name:** Stop Market Order

```json
{
  "Quantity": "10",
  "StopPrice": "50.60"
}
```

---

### Example 43: PUT /v3/orderexecution/orders/{orderID}

**Example Name:** Stop Limit Order

```json
{
  "Quantity": "10",
  "LimitPrice": "200.00",
  "StopPrice": "215.00"
}
```

---

### Example 44: PUT /v3/orderexecution/orders/{orderID}

**Example Name:** Trailing Stop (Amount)

```json
{
  "Quantity": "10",
  "AdvancedOptions": {
    "TrailingStop": {
      "Amount": "2.11"
    }
  }
}
```

---

### Example 45: PUT /v3/orderexecution/orders/{orderID}

**Example Name:** Trailing Stop (Percent)

```json
{
  "Quantity": "10",
  "AdvancedOptions": {
    "TrailingStop": {
      "Percent": "5.0"
    }
  }
}
```

---

### Example 46: PUT /v3/orderexecution/orders/{orderID}

**Example Name:** Convert to Market

```json
{
  "OrderType": "Market"
}
```

---

## Node Examples

### Example 1: GET /v2/data/symbols/suggest/{text}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v2/data/symbols/suggest/{text}',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 2: GET /v2/data/symbols/search/{criteria}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v2/data/symbols/search/{criteria}',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 3: GET /v2/stream/tickbars/{symbol}/{interval}/{barsBack}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v2/stream/tickbars/{symbol}/{interval}/{barsBack}',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 4: GET /v3/brokerage/accounts

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 5: GET /v3/brokerage/accounts/{accounts}/balances

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/balances',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 6: GET /v3/brokerage/accounts/{accounts}/bodbalances

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/bodbalances',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 7: GET /v3/brokerage/accounts/{accounts}/historicalorders

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders',
  qs: {since: '2006-01-13'},
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 8: GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders/123456789,286179863',
  qs: {since: '2006-01-13'},
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 9: GET /v3/brokerage/accounts/{accounts}/orders

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 10: GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders/123456789,286179863',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 11: GET /v3/brokerage/accounts/{accounts}/positions

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/positions',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 12: POST /v3/orderexecution/orderconfirm

```node
const request = require('request');

const options = {
  method: 'POST',
  url: 'https://api.tradestation.com/v3/orderexecution/orderconfirm',
  headers: {'content-type': 'application/json', Authorization: 'Bearer TOKEN'},
  body: {
    AccountID: '123456782',
    Symbol: 'MSFT',
    Quantity: '10',
    OrderType: 'Market',
    TradeAction: 'BUY',
    TimeInForce: {Duration: 'DAY'},
    Route: 'Intelligent'
  },
  json: true
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 13: POST /v3/orderexecution/ordergroupconfirm

```node
const request = require('request');

const options = {
  method: 'POST',
  url: 'https://api.tradestation.com/v3/orderexecution/ordergroupconfirm',
  headers: {'content-type': 'application/json', Authorization: 'Bearer TOKEN'},
  body: {
    Type: 'OCO',
    Orders: [
      {
        AccountID: '123456782',
        StopPrice: '337',
        OrderType: 'StopMarket',
        Quantity: '10',
        Route: 'Intelligent',
        Symbol: 'MSFT',
        TimeInForce: {Duration: 'GTC'},
        TradeAction: 'Buy'
      },
      {
        AccountID: '123456782',
        StopPrice: '333',
        OrderType: 'StopMarket',
        Quantity: '10',
        Route: 'Intelligent',
        Symbol: 'MSFT',
        TimeInForce: {Duration: 'GTC'},
        TradeAction: 'SellShort'
      }
    ]
  },
  json: true
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 14: POST /v3/orderexecution/ordergroups

```node
const request = require('request');

const options = {
  method: 'POST',
  url: 'https://api.tradestation.com/v3/orderexecution/ordergroups',
  headers: {'content-type': 'application/json', Authorization: 'Bearer TOKEN'},
  body: {
    Type: 'OCO',
    Orders: [
      {
        AccountID: '123456782',
        StopPrice: '337',
        OrderType: 'StopMarket',
        Quantity: '10',
        Route: 'Intelligent',
        Symbol: 'MSFT',
        TimeInForce: {Duration: 'GTC'},
        TradeAction: 'Buy'
      },
      {
        AccountID: '123456782',
        StopPrice: '333',
        OrderType: 'StopMarket',
        Quantity: '10',
        Route: 'Intelligent',
        Symbol: 'MSFT',
        TimeInForce: {Duration: 'GTC'},
        TradeAction: 'SellShort'
      }
    ]
  },
  json: true
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 15: POST /v3/orderexecution/orders

```node
const request = require('request');

const options = {
  method: 'POST',
  url: 'https://api.tradestation.com/v3/orderexecution/orders',
  headers: {'content-type': 'application/json', Authorization: 'Bearer TOKEN'},
  body: {
    AccountID: '123456782',
    Symbol: 'MSFT',
    Quantity: '10',
    OrderType: 'Market',
    TradeAction: 'BUY',
    TimeInForce: {Duration: 'DAY'},
    Route: 'Intelligent'
  },
  json: true
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 16: PUT /v3/orderexecution/orders/{orderID}

```node
const request = require('request');

const options = {
  method: 'PUT',
  url: 'https://api.tradestation.com/v3/orderexecution/orders/123456789',
  headers: {'content-type': 'application/json', Authorization: 'Bearer TOKEN'},
  body: {Quantity: '10', LimitPrice: '132.52'},
  json: true
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 17: DELETE /v3/orderexecution/orders/{orderID}

```node
const request = require('request');

const options = {
  method: 'DELETE',
  url: 'https://api.tradestation.com/v3/orderexecution/orders/123456789',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 18: GET /v3/marketdata/barcharts/{symbol}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/barcharts/MSFT',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 19: GET /v3/marketdata/stream/barcharts/{symbol}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/stream/barcharts/MSFT',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 20: GET /v3/marketdata/symbollists/cryptopairs/symbolnames

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/symbollists/cryptopairs/symbolnames',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 21: GET /v3/marketdata/symbols/{symbols}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/symbols/MSFT,BTCUSD',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 22: GET /v3/orderexecution/activationtriggers

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/orderexecution/activationtriggers',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 23: GET /v3/orderexecution/routes

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/orderexecution/routes',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 24: GET /v3/marketdata/options/expirations/{underlying}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/options/expirations/AAPL',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 25: POST /v3/marketdata/options/riskreward

```node
const request = require('request');

const options = {
  method: 'POST',
  url: 'https://api.tradestation.com/v3/marketdata/options/riskreward',
  headers: {'content-type': 'application/json', Authorization: 'Bearer TOKEN'},
  body: {SpreadPrice: 0.1, Legs: [{Symbol: 'string', Quantity: 0, TradeAction: 'BUY'}]},
  json: true
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 26: GET /v3/marketdata/options/spreadtypes

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/options/spreadtypes',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 27: GET /v3/marketdata/options/strikes/{underlying}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/options/strikes/AAPL',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 28: GET /v3/marketdata/stream/options/chains/{underlying}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/stream/options/chains/AAPL',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 29: GET /v3/marketdata/stream/options/quotes

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/stream/options/quotes',
  qs: {'legs[0].Symbol': 'MSFT 220916C305'},
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 30: GET /v3/marketdata/quotes/{symbols}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/quotes/MSFT,BTCUSD',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

---

### Example 31: GET /v3/marketdata/stream/quotes/{symbols}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/stream/quotes/MSFT,BTCUSD',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 32: GET /v3/marketdata/stream/marketdepth/quotes/{symbol}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/stream/marketdepth/quotes/MSFT',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 33: GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/marketdata/stream/marketdepth/aggregates/MSFT',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 34: GET /v3/brokerage/stream/accounts/{accounts}/orders

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 35: GET /v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders/812767578,812941051',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

### Example 36: GET /v3/brokerage/stream/accounts/{accounts}/positions

```node
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/positions',
  headers: {Authorization: 'Bearer TOKEN'}
};

request(options).on('data', function (data) {
  console.log(data.toString());
}).on('error', function(err) {
  console.error(err)
});

```

---

## Python Examples

### Example 1: GET /v2/data/symbols/suggest/{text}

```python
import requests

url = "https://api.tradestation.com/v2/data/symbols/suggest/{text}"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 2: GET /v2/data/symbols/search/{criteria}

```python
import requests

url = "https://api.tradestation.com/v2/data/symbols/search/{criteria}"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 3: GET /v2/stream/tickbars/{symbol}/{interval}/{barsBack}

```python
import requests

url = "https://api.tradestation.com/v2/stream/tickbars/{symbol}/{interval}/{barsBack}"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 4: GET /v3/brokerage/accounts

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 5: GET /v3/brokerage/accounts/{accounts}/balances

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/balances"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 6: GET /v3/brokerage/accounts/{accounts}/bodbalances

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/bodbalances"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 7: GET /v3/brokerage/accounts/{accounts}/historicalorders

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders"

querystring = {"since":"2006-01-13"}

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
```

---

### Example 8: GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders/123456789,286179863"

querystring = {"since":"2006-01-13"}

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
```

---

### Example 9: GET /v3/brokerage/accounts/{accounts}/orders

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 10: GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders/123456789,286179863"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 11: GET /v3/brokerage/accounts/{accounts}/positions

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/positions"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 12: POST /v3/orderexecution/orderconfirm

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/orderconfirm"

payload = {
    "AccountID": "123456782",
    "Symbol": "MSFT",
    "Quantity": "10",
    "OrderType": "Market",
    "TradeAction": "BUY",
    "TimeInForce": {"Duration": "DAY"},
    "Route": "Intelligent"
}
headers = {
    "content-type": "application/json",
    "Authorization": "Bearer TOKEN"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

---

### Example 13: POST /v3/orderexecution/ordergroupconfirm

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/ordergroupconfirm"

payload = {
    "Type": "OCO",
    "Orders": [
        {
            "AccountID": "123456782",
            "StopPrice": "337",
            "OrderType": "StopMarket",
            "Quantity": "10",
            "Route": "Intelligent",
            "Symbol": "MSFT",
            "TimeInForce": {"Duration": "GTC"},
            "TradeAction": "Buy"
        },
        {
            "AccountID": "123456782",
            "StopPrice": "333",
            "OrderType": "StopMarket",
            "Quantity": "10",
            "Route": "Intelligent",
            "Symbol": "MSFT",
            "TimeInForce": {"Duration": "GTC"},
            "TradeAction": "SellShort"
        }
    ]
}
headers = {
    "content-type": "application/json",
    "Authorization": "Bearer TOKEN"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

---

### Example 14: POST /v3/orderexecution/ordergroups

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/ordergroups"

payload = {
    "Type": "OCO",
    "Orders": [
        {
            "AccountID": "123456782",
            "StopPrice": "337",
            "OrderType": "StopMarket",
            "Quantity": "10",
            "Route": "Intelligent",
            "Symbol": "MSFT",
            "TimeInForce": {"Duration": "GTC"},
            "TradeAction": "Buy"
        },
        {
            "AccountID": "123456782",
            "StopPrice": "333",
            "OrderType": "StopMarket",
            "Quantity": "10",
            "Route": "Intelligent",
            "Symbol": "MSFT",
            "TimeInForce": {"Duration": "GTC"},
            "TradeAction": "SellShort"
        }
    ]
}
headers = {
    "content-type": "application/json",
    "Authorization": "Bearer TOKEN"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

---

### Example 15: POST /v3/orderexecution/orders

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/orders"

payload = {
    "AccountID": "123456782",
    "Symbol": "MSFT",
    "Quantity": "10",
    "OrderType": "Market",
    "TradeAction": "BUY",
    "TimeInForce": {"Duration": "DAY"},
    "Route": "Intelligent"
}
headers = {
    "content-type": "application/json",
    "Authorization": "Bearer TOKEN"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

---

### Example 16: PUT /v3/orderexecution/orders/{orderID}

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/orders/123456789"

payload = {
    "Quantity": "10",
    "LimitPrice": "132.52"
}
headers = {
    "content-type": "application/json",
    "Authorization": "Bearer TOKEN"
}

response = requests.request("PUT", url, json=payload, headers=headers)

print(response.text)
```

---

### Example 17: DELETE /v3/orderexecution/orders/{orderID}

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/orders/123456789"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("DELETE", url, headers=headers)

print(response.text)
```

---

### Example 18: GET /v3/marketdata/barcharts/{symbol}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/barcharts/MSFT"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 19: GET /v3/marketdata/stream/barcharts/{symbol}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/stream/barcharts/MSFT"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 20: GET /v3/marketdata/symbollists/cryptopairs/symbolnames

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/symbollists/cryptopairs/symbolnames"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 21: GET /v3/marketdata/symbols/{symbols}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/symbols/MSFT,BTCUSD"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 22: GET /v3/orderexecution/activationtriggers

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/activationtriggers"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 23: GET /v3/orderexecution/routes

```python
import requests

url = "https://api.tradestation.com/v3/orderexecution/routes"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 24: GET /v3/marketdata/options/expirations/{underlying}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/options/expirations/AAPL"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 25: POST /v3/marketdata/options/riskreward

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/options/riskreward"

payload = {
    "SpreadPrice": 0.1,
    "Legs": [
        {
            "Symbol": "string",
            "Quantity": 0,
            "TradeAction": "BUY"
        }
    ]
}
headers = {
    "content-type": "application/json",
    "Authorization": "Bearer TOKEN"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

---

### Example 26: GET /v3/marketdata/options/spreadtypes

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/options/spreadtypes"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 27: GET /v3/marketdata/options/strikes/{underlying}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/options/strikes/AAPL"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 28: GET /v3/marketdata/stream/options/chains/{underlying}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/stream/options/chains/AAPL"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 29: GET /v3/marketdata/stream/options/quotes

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/stream/options/quotes"

querystring = {"legs[0].Symbol":"MSFT 220916C305"}

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, params=querystring, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 30: GET /v3/marketdata/quotes/{symbols}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/quotes/MSFT,BTCUSD"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

---

### Example 31: GET /v3/marketdata/stream/quotes/{symbols}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/stream/quotes/MSFT,BTCUSD"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 32: GET /v3/marketdata/stream/marketdepth/quotes/{symbol}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/stream/marketdepth/quotes/MSFT"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 33: GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}

```python
import requests

url = "https://api.tradestation.com/v3/marketdata/stream/marketdepth/aggregates/MSFT"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 34: GET /v3/brokerage/stream/accounts/{accounts}/orders

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 35: GET /v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders/812767578,812941051"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

### Example 36: GET /v3/brokerage/stream/accounts/{accounts}/positions

```python
import requests

url = "https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/positions"

headers = {"Authorization": "Bearer TOKEN"}

response = requests.request("GET", url, headers=headers, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
```

---

## Shell Examples

### Example 1: GET /v2/data/symbols/suggest/{text}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v2/data/symbols/suggest/{text}' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 2: GET /v2/data/symbols/search/{criteria}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v2/data/symbols/search/{criteria}' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 3: GET /v2/stream/tickbars/{symbol}/{interval}/{barsBack}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v2/stream/tickbars/{symbol}/{interval}/{barsBack}' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 4: GET /v3/brokerage/accounts

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 5: GET /v3/brokerage/accounts/{accounts}/balances

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/balances' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 6: GET /v3/brokerage/accounts/{accounts}/bodbalances

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/bodbalances' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 7: GET /v3/brokerage/accounts/{accounts}/historicalorders

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders?since=2006-01-13' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 8: GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/historicalorders/123456789,286179863?since=2006-01-13' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 9: GET /v3/brokerage/accounts/{accounts}/orders

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 10: GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/orders/123456789,286179863' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 11: GET /v3/brokerage/accounts/{accounts}/positions

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/accounts/61999124,68910124/positions' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 12: POST /v3/orderexecution/orderconfirm

```shell
curl --request POST \
  --url 'https://api.tradestation.com/v3/orderexecution/orderconfirm' \
  --header 'Authorization: Bearer TOKEN' \
  --header 'content-type: application/json' \
  --data '{"AccountID":"123456782","Symbol":"MSFT","Quantity":"10","OrderType":"Market","TradeAction":"BUY","TimeInForce":{"Duration":"DAY"},"Route":"Intelligent"}'
```

---

### Example 13: POST /v3/orderexecution/ordergroupconfirm

```shell
curl --request POST \
  --url 'https://api.tradestation.com/v3/orderexecution/ordergroupconfirm' \
  --header 'Authorization: Bearer TOKEN' \
  --header 'content-type: application/json' \
  --data '{"Type":"OCO","Orders":[{"AccountID":"123456782","StopPrice":"337","OrderType":"StopMarket","Quantity":"10","Route":"Intelligent","Symbol":"MSFT","TimeInForce":{"Duration":"GTC"},"TradeAction":"Buy"},{"AccountID":"123456782","StopPrice":"333","OrderType":"StopMarket","Quantity":"10","Route":"Intelligent","Symbol":"MSFT","TimeInForce":{"Duration":"GTC"},"TradeAction":"SellShort"}]}'
```

---

### Example 14: POST /v3/orderexecution/ordergroups

```shell
curl --request POST \
  --url 'https://api.tradestation.com/v3/orderexecution/ordergroups' \
  --header 'Authorization: Bearer TOKEN' \
  --header 'content-type: application/json' \
  --data '{"Type":"OCO","Orders":[{"AccountID":"123456782","StopPrice":"337","OrderType":"StopMarket","Quantity":"10","Route":"Intelligent","Symbol":"MSFT","TimeInForce":{"Duration":"GTC"},"TradeAction":"Buy"},{"AccountID":"123456782","StopPrice":"333","OrderType":"StopMarket","Quantity":"10","Route":"Intelligent","Symbol":"MSFT","TimeInForce":{"Duration":"GTC"},"TradeAction":"SellShort"}]}'
```

---

### Example 15: POST /v3/orderexecution/orders

```shell
curl --request POST \
  --url 'https://api.tradestation.com/v3/orderexecution/orders' \
  --header 'Authorization: Bearer TOKEN' \
  --header 'content-type: application/json' \
  --data '{"AccountID":"123456782","Symbol":"MSFT","Quantity":"10","OrderType":"Market","TradeAction":"BUY","TimeInForce":{"Duration":"DAY"},"Route":"Intelligent"}'
```

---

### Example 16: PUT /v3/orderexecution/orders/{orderID}

```shell
curl --request PUT \
  --url 'https://api.tradestation.com/v3/orderexecution/orders/123456789' \
  --header 'Authorization: Bearer TOKEN' \
  --header 'content-type: application/json' \
  --data '{"Quantity":"10","LimitPrice":"132.52"}'
```

---

### Example 17: DELETE /v3/orderexecution/orders/{orderID}

```shell
curl --request DELETE \
  --url 'https://api.tradestation.com/v3/orderexecution/orders/123456789' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 18: GET /v3/marketdata/barcharts/{symbol}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/barcharts/MSFT' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 19: GET /v3/marketdata/stream/barcharts/{symbol}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/stream/barcharts/MSFT' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 20: GET /v3/marketdata/symbollists/cryptopairs/symbolnames

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/symbollists/cryptopairs/symbolnames' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 21: GET /v3/marketdata/symbols/{symbols}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/symbols/MSFT,BTCUSD' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 22: GET /v3/orderexecution/activationtriggers

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/orderexecution/activationtriggers' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 23: GET /v3/orderexecution/routes

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/orderexecution/routes' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 24: GET /v3/marketdata/options/expirations/{underlying}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/options/expirations/AAPL' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 25: POST /v3/marketdata/options/riskreward

```shell
curl --request POST \
  --url 'https://api.tradestation.com/v3/marketdata/options/riskreward' \
  --header 'Authorization: Bearer TOKEN' \
  --header 'content-type: application/json' \
  --data '{"SpreadPrice":0.1,"Legs":[{"Symbol":"string","Quantity":0,"TradeAction":"BUY"}]}'
```

---

### Example 26: GET /v3/marketdata/options/spreadtypes

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/options/spreadtypes' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 27: GET /v3/marketdata/options/strikes/{underlying}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/options/strikes/AAPL' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 28: GET /v3/marketdata/stream/options/chains/{underlying}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/stream/options/chains/AAPL' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 29: GET /v3/marketdata/stream/options/quotes

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/stream/options/quotes?legs%5B0%5D.Symbol=MSFT%20220916C305' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 30: GET /v3/marketdata/quotes/{symbols}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/quotes/MSFT,BTCUSD' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 31: GET /v3/marketdata/stream/quotes/{symbols}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/stream/quotes/MSFT,BTCUSD' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 32: GET /v3/marketdata/stream/marketdepth/quotes/{symbol}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/stream/marketdepth/quotes/MSFT' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 33: GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/marketdata/stream/marketdepth/aggregates/MSFT' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 34: GET /v3/brokerage/stream/accounts/{accounts}/orders

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 35: GET /v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/orders/812767578,812941051' \
  --header 'Authorization: Bearer TOKEN'
```

---

### Example 36: GET /v3/brokerage/stream/accounts/{accounts}/positions

```shell
curl --request GET \
  --url 'https://api.tradestation.com/v3/brokerage/stream/accounts/61999124,68910124/positions' \
  --header 'Authorization: Bearer TOKEN'
```

---

