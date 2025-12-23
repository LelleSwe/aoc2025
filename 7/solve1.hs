step :: (Bool, Int, [Int]) -> String -> [Int] -> (Int, [Int])
step (_, accum, state) "" prev = (accum, state)
step (prev, prevAccum, state) (s : ss) (x : xs) = step (next, accum, f (s, x) state) ss xs
  where
    f (a, b) state
      | a == '.' && prev = state ++ [1]
      | a == '.' = state ++ [b]
      | a == '^' && b == 1 = init state ++ [1, 0]
      | a == '^' && b == 0 = state ++ [0]
      | a == 'S' = state ++ [1]
    next = s == '^' && x == 1
    accum = if s == '^' && x == 1 then prevAccum + 1 else prevAccum

loopOver :: Int -> [Int] -> [String] -> Int
loopOver accum _ [] = accum
loopOver accum state (x : xs) =
  let (a, b) = step (False, 0, []) x state
   in loopOver (a + accum) b xs

readlines :: IO [String]
readlines = lines <$> getContents

main :: IO () = do
  io <- readlines
  print $ loopOver 0 (replicate (length . head $ io) 0) io
