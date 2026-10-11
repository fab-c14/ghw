SELECT symbol, count(*) AS ticks,
       round(min(price)::numeric, 2) AS low,
       round(max(price)::numeric, 2) AS high
FROM crypto_ticks
GROUP BY symbol
ORDER BY symbol;

SELECT bucket, symbol,
       round(open::numeric, 2) AS open,
       round(high::numeric, 2) AS high,
       round(low::numeric, 2) AS low,
       round(close::numeric, 2) AS close
FROM one_minute_candle
ORDER BY bucket DESC, symbol
LIMIT 6;
