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

remove :: (Int, Int) -> [[Int]] -> [[Int]]
remove (x, y) inp = take y inp ++ [(take x $ inp !! y) ++ [0] ++ (drop (x + 1) $ inp !! y)] ++ drop (y + 1) inp

-- make sure to start at 0,0 ig
loopOver :: (Int, Int) -> (Int, [[Int]]) -> (Int, [[Int]])
loopOver (x, y) (state, inp)
  | x >= length (head inp) = loopOver (0, y + 1) (state, inp)
  | y >= length inp = (state, inp)
  | get (x, y) inp == 1 && getAdj (x, y) inp < 4 = (state + 1, remove (x, y) inp)
  | otherwise = loopOver (x + 1, y) (state, inp)

sol :: [[Int]] -> Int
sol inp = if next /= inp then ans + sol next else ans
  where
    (ans, next) = loopOver (0, 0) (0, inp)

main :: IO () = do
  io <- readlinesStr
  let inp = preProcess io
  print $ sol inp
