readlinesStr :: IO [String]
readlinesStr = lines <$> getContents

preProcess :: [String] -> [[Int]]
preProcess = map $ map (\x -> if x == '@' then 1 else 0)

-- maybe switch to vector/array so don't have O(n) lookup?
-- holy get spam :cold_face:
getAdj :: (Int, Int) -> [[Int]] -> Int
getAdj (x, y) inp =
  get (x + 1, y) inp
    + get (x + 1, y + 1) inp
    + get (x + 1, y - 1) inp
    + get (x, y + 1) inp
    + get (x, y - 1) inp
    + get (x - 1, y + 1) inp
    + get (x - 1, y) inp
    + get (x - 1, y - 1) inp

get :: (Int, Int) -> [[Int]] -> Int
get (x, y) inp
  | x < 0 = 0
  | x >= length (head inp) = 0
  | y < 0 = 0
  | y >= length inp = 0
  | otherwise = inp !! y !! x

xD :: (Int, Int) -> [[Int]] -> Int -> Int
xD (x, y) inp current
  | current == 0 = 0
  | x < 0 = 0
  | x >= length (head inp) = 0
  | otherwise = inp !! y !! x + xD (x + 1, y) inp (current - 1)

yD :: (Int, Int) -> [[Int]] -> Int -> Int
yD (x, y) inp current
  | current == 0 = 0
  | y < 0 = 0
  | y >= length inp = 0
  | otherwise = inp !! y !! x + xD (x, y + 1) inp (current - 1)

-- make sure to start at 0,0 ig
sol :: Int -> (Int, Int) -> [[Int]] -> Int
sol state (x, y) inp
  | x >= length (head inp) = sol state (0, y + 1) inp
  | y >= length inp = state
  | otherwise = if get (x, y) inp == 1 && getAdj (x, y) inp < 4 then sol (state + 1) (x + 1, y) inp else sol state (x + 1, y) inp

main :: IO () = do
  io <- readlinesStr
  let inp = preProcess io
  print $ sol 0 (0, 0) inp
