-- feels like you can do some segment tree black magic here,
-- but haven't thought too much about it
import Data.List.Split

readlinesStr :: IO [String]
readlinesStr = lines <$> getContents

ff :: [String] -> ([String], [String])
ff = f . splitOn [""]
  where
    f a = (head a, a !! 1)

toRanges :: [String] -> [(Int, Int)]
toRanges = map (int . f . splitOn "-")
  where
    int (x, y) = (read x, read y)
    f a = (head a, a !! 1)

toInts :: [String] -> [Int]
toInts = map read

validOne :: Int -> [(Int, Int)] -> Bool
validOne i ((l, r) : xs)
  | l <= i && i <= r = True
  | null xs = False
  | otherwise = validOne i xs

validAll :: [Int] -> [(Int, Int)] -> Int
validAll ints ranges = sum $ map (fromEnum . (`validOne` ranges)) ints

main :: IO () = do
  io <- readlinesStr
  let ranges = (toRanges . fst . ff) io
      ints = (toInts . snd . ff) io
  -- print ranges
  -- print ints
  print $ validAll ints ranges
