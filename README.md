# AcademicProject-1
The yield curve and pricing of mortgages

We were interested in investigating how the shape of the yield curve can affect the prices of specified mortgage pools.

Specified Pools : 
Monthly futures contracts trade for 30 year mortgage pass through bonds. The futures contract specifies what coupon needs to be delivered, but within that coupon there is some flexibility.  We looked at pools.  We looked at the pricing of pools, all with the same coupon, but different ages.

Yield Curve : 
The treasury yield curve displays the market clearing yields for treasury bonds of different maturity. For bonds of the same coupon, this translates into different prices for different maturities.  Under a given prepayment assumption all 30 year mortgages have very similar maturities but these can vary with slight changes in age.

Methodology : 
We used CMO (Front / Back sequential ) excitation to price the pools of various ages.   Our methodology was as follows.  
CMOs buyers are concerned with the average life of the font bond at a slow (+300) prepayment speed. This average life constraint we treat as an input.  For each age pool we can then devise the front / back allocation to produce similar looking front sequential CMOs.    
The back sequential trades on a spread to the curve basis.  We treat this spread to the curve as an  input as well.
We use the price of a TBA (assumed to be 0 age) as an input as well.
With the above inputs, maintaining constant spread to the curve on the front sequential we are able to derive prices for pools of age 0 to 30.  


 

