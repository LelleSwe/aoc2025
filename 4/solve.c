#include <stdio.h>

static int state[136][136];
static int ans = 0;

int get_adj(int x, int y) {
   int tot = 0;
   for (int dx = -1; dx <= 1; dx++) {
      for (int dy = -1; dy <= 1; dy++) {
         if ((x + dx < 0) || (x + dx >= 136) || (y + dy < 0) ||
             (y + dy >= 136) || ((dx == 0) && (dy == 0)))
            continue;
         tot += state[y + dy][x + dx];
      }
   }
   return tot;
}

void search_adj(int x, int y) {
   ans++;
   state[y][x] = 0;
   for (int dx = -1; dx <= 1; dx++) {
      for (int dy = -1; dy <= 1; dy++) {
         if ((x + dx < 0) || (x + dx >= 136) || (y + dy < 0) ||
             (y + dy >= 136)) {
            continue;
         }
         if ((get_adj(x + dx, y + dy) < 4) && (state[y + dy][x + dx])) {
            search_adj(x + dx, y + dy);
         }
      }
   }
}

void read() {
   char inp[138];
   for (int i = 0; i < 136; i++) {
      // bruh why 138 why are you like this
      // ohhhhhh because 136 chars + LF + null terminator
      // okay that actually makes sense
      fgets(inp, 138, stdin);
      // printf("%d %s\n", i, inp);

      for (int ii = 0; ii < 136; ii++) {
         if (inp[ii] == '@') {
            state[i][ii] = 1;
         } else {
            state[i][ii] = 0;
         }
      }
   }
}

void search_all() {
   // for (int i = 0; i < 120; i++) {
   int cur = ans;
   for (int x = 0; x < 136; x++) {
      for (int y = 0; y < 136; y++) {
         if ((get_adj(x, y) < 4) && state[y][x]) {
            search_adj(x, y);
            // ans++;
            // state[y][x] = 0;
         }
      }
   }
   // printf("%d %d\n", ans, cur);
   // if (ans != cur) {
   //    search_all();
   // }
}

int main() {
   read();
   search_all();

   printf("%d\n", ans);

   return 0;
}
