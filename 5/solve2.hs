-- feels like you can do some segment tree black magic here,
-- but haven't thought too much about it
import Data.List.Split

readlinesStr :: IO [String]
readlinesStr = lines <$> getContents

ff :: [String] -> ([String], [String])
ff = f . splitOn [""]
 where
  f a = (head a, a !! 1)

toRanges :: [String] -> [(Integer, Integer)]
toRanges = map (int . f . splitOn "-")
 where
  int (x, y) = (read x, read y)
  f a = (head a, a !! 1)

sortBy :: (Ord a) => (a -> a -> Bool) -> [a] -> [a]
sortBy key [] = []
sortBy key (x : xs) = (sortBy key [y | y <- xs, key y x]) ++ [x] ++ sortBy key [y | y <- xs, not $ key y x]

sortRanges :: [(Integer, Integer)] -> [(Integer, Integer)]
sortRanges = sortBy (\(x1, y1) (x2, y2) -> (if x1 == x2 then y1 < y2 else x1 < x2))

trimRange :: Integer -> (Integer, Integer) -> (Integer, (Integer, Integer))
trimRange rm (l, r)
  | rm >= r = (nrm, (0, 0))
  | (rm >= l) && (rm < r) = (nrm, (rm+1, r))
  | otherwise = (nrm, (l, r))
  where nrm = max rm r
  -- ig testdatan bara testade aldrig fall där det finns en range som strikt innehåller en annan?
  -- liksom (1, 5) och (2, 4). (1, 5) innehåller mer än hela den andra
  -- men svaret ändrades inte
  -- motsvarande (1, 5) och (1, 4) fanns, men inte med strikt olikhet på båda
  -- | l1 == l2 = (0, 0)
  -- | r1 >= l2 && r1 <= r2 = (l1, l2-1)
-- | r1 > r2 = (l1, r1)

trunc :: Integer -> [(Integer, Integer)] -> [(Integer, Integer)]
trunc rm_ [x] = [snd $ trimRange rm_ x]
trunc rm_ (x : xs) = out : trunc rm xs
  where (rm, out) = trimRange rm_ x

tot :: [(Integer, Integer)] -> Integer
tot = sum . map fsum
  where
  -- jag kommer crasha ut så hårt buggen var att jag hade l == r 
  -- men det fanns ett fall med det i indatan som då tolkades fel
    fsum (l, r) = if l == 0 && r == 0 then 0 else r-l+1

main :: IO () = do
  io <- readlinesStr
  let ranges = (toRanges . fst . ff) io
  -- print ranges
  -- print ints
  print $ tot . trunc 0 . sortRanges . toRanges . fst . ff $ io
