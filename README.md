# Tradebot
Just a trading bot to make passive income. This uses an alogrithm that I designed and developed. This strategy uses no indicators as the more I learn about the markets the more I realize that there is no need for indicators and if anything indicators blind you from seeing price action. 

## How does it work
This is a quite simple strategy where it simply just looks at if we have a break in market structure and if we are in an uptrend or in a downtrend and depending on that an order can be placed. The uptrend and downtrend checking is just simply if over the past couple of highs and lows are we making higher highs and higher lows or is it lower lows and lower highs indicating a bullish trend or a bearish trend respectively. 

## Functions
Order.py has been modtified from main branch
The main branch is dog shit but left it because there may be a time where I have to go back to where I began

Better_test branch
Order.buyorsell() 
- Enters on trade every time the prehigh or prelow has been broken (means that could have a sell open but then enter on another sell order)
  
Order.watch()
- standard watch
- close half at 10 pips profit and 10 pips stoploss
- goes up 6 pips move stop loss to break even
- closes full postition at full take profit(25 pips)
- closes full position at full stop loss (opening low wick)
- make sure that len() stuff has been fixed
 
Nextmod branch
Order.buyorsell()
- Enters only once on a trade (if a sell order is already in effect another one will not be opened

Order.watch()
- slightly modified watch (takes everything from better_test branch Order.watch()
- close half at 10 pips profit and 10 pips stoploss
- goes up 6 pips move stop loss to break even
- closes full position at full stop loss (opening low wick)
- doesn't have a take profit anymore relies on hitting stoploss
- every 30 minute candle with the coresponding color close moves stop loss to the low of that candle
- in other words if opened a buy then once it moves to 6 pips moves stop loss to break even, then at 10 pips closes half positions, then after that we wait for the current candle to close and then we wait another 30m close if it's green then we move our stop loss to the low of that candle(as long as the low isn't lower than our current stop loss) and this proccess continues all the way until it hits our stop loss. This makes sure that we can catch the really big movements without risking too much.
