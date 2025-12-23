import Data.Char (isSpace)
import Data.List
import Data.List.Split

trim :: String -> String
trim = f . f
  where
    f = reverse . dropWhile isSpace

getlines :: IO [String]
getlines = lines <$> getContents

getIndices_ :: String -> (Int, [Int]) -> [Int]
getIndices_ "" (_, state) = state
getIndices_ (x : xs) (len, state) = if x == ' ' then getIndices_ xs (len + 1, state) else len : getIndices_ xs (1, state)

getIndices :: String -> [Int]
getIndices = (`getIndices_` (0, []))

concatInt :: String -> Integer
concatInt inp = read [a | a <- inp, a /= ' ']

------------------------------------------------

nums_ :: (String -> a) -> String -> [Int] -> [a]
nums_ f inp [x] = [f a, f b]
  where
    (a, b) = splitAt x inp
nums_ f inp lens = (f $ fst w) : nums_ f (snd w) (tail lens)
  where
    w = splitAt (head lens) inp

nums :: (String -> a) -> [Int] -> String -> [a]
nums f lens = (`abc` tail lens)
  where
    abc = nums_ f

getops :: [Int] -> String -> [(Integer, Integer -> Integer -> Integer)]
getops lens inp = map f (nums id lens inp)
  where
    f a
      | trim a == "+" = (0, (+))
      | trim a == "*" = (1, (*))
      | otherwise = error "ops failed"

----------------------------------------------------

rnums :: Int -> [String] -> [[Integer]]
rnums len = map (map concatInt) . splitOn [replicate len ' '] . transpose

calc :: [(Integer, Integer -> Integer -> Integer)] -> [[Integer]] -> [Integer]
calc ops inp = [foldl op identity abc | ((identity, op), abc) <- zip ops inp]

main :: IO () = do
  io <- getlines
  let lens = getIndices . last $ io
  let ops = getops lens . last $ io
  print $ sum . calc ops . rnums (length . head . transpose . init $ io) . init $ io
