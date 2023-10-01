#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

const long long max_size = 2000;         // max length of strings
const long long N = 40;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries

// run by ./distance intm/vector_qnum.bin intm/nw_qnum.txt word
// appends top N words to file intm/nw_qnum.txt
int main(int argc, char **argv) {
  FILE *f;
  char st1[max_size];
  char outfile[max_size];
  char *bestw[N];
  char file_name[max_size], st[100][max_size];
  float dist, len, bestd[N], vec[max_size];
  long long words, size, a, b, c, d, cn, bi[100];
  char ch;
  float *M;
  char *vocab;
  if (argc < 3) {
    printf("Usage: ./distance <FILE> <word>\nwhere FILE contains word projections in the BINARY FORMAT\n");
    return 0;
  }
  strcpy(file_name, argv[1]);
  f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    return -1;
  }
  fscanf(f, "%lld", &words);
  fscanf(f, "%lld", &size);
  vocab = (char *)malloc((long long)words * max_w * sizeof(char));
  for (a = 0; a < N; a++) bestw[a] = (char *)malloc(max_size * sizeof(char));
  M = (float *)malloc((long long)words * (long long)size * sizeof(float));
  if (M == NULL) {
    printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)words * size * sizeof(float) / 1048576, words, size);
    return -1;
  }
  for (b = 0; b < words; b++) {
    a = 0;
    while (1) {
      vocab[b * max_w + a] = fgetc(f);
      if (feof(f) || (vocab[b * max_w + a] == ' ')) break;
      if ((a < max_w) && (vocab[b * max_w + a] != '\n')) a++;
    }
    vocab[b * max_w + a] = 0;
    for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
    len = 0;
    for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
    len = sqrt(len);
    for (a = 0; a < size; a++) M[a + b * size] /= len;
  }
  fclose(f);
  //while (1) {
    for (a = 0; a < N; a++) bestd[a] = 0;
    for (a = 0; a < N; a++) bestw[a][0] = 0;
    //printf("Enter word or sentence (EXIT to break): ");
    a = 0;
    strcpy(st1, argv[3]);
    strcpy(outfile, argv[2]);

    //size_t lengthi = strlen(st1);
    //st1[lengthi] = '0';
    //st1[lengthi + 1] = '\0';

    //   while (1) {
    //   st1[a] = fgetc(stdin);
    //   if ((st1[a] == '\n') || (a >= max_size - 1)) {
    //     st1[a] = 0;
    //     break;
    //   }
    //   a++;
    // }
    //if (!strcmp(st1, "EXIT")) break;
    cn = 0;
    b = 0;
    c = 0;
    while (1) {
      st[cn][b] = st1[c];
      b++;
      c++;
      st[cn][b] = 0;
      if (st1[c] == 0) break;
      if (st1[c] == ' ') {
        cn++;
        b = 0;
        c++;
      }
    }
    cn++;
    for (a = 0; a < cn; a++) {
      for (b = 0; b < words; b++) if (!strcmp(&vocab[b * max_w], st[a])) break;
      if (b == words) b = -1;
      bi[a] = b;
      printf("\nWord: %s  Position in vocabulary: %lld\n", st[a], bi[a]);
      if (b == -1) {
        printf("Out of dictionary word!\n");
        break;
      }
    }
    if (b >= 0){
      printf("\n                                              Word       Cosine distance\n------------------------------------------------------------------------\n");
      for (a = 0; a < size; a++) vec[a] = 0;
      for (b = 0; b < cn; b++) {
        if (bi[b] == -1) continue;
        for (a = 0; a < size; a++) vec[a] += M[a + bi[b] * size];
      }
      //printf("here1\n");
      len = 0;
      for (a = 0; a < size; a++) len += vec[a] * vec[a];
      len = sqrt(len);
      for (a = 0; a < size; a++) vec[a] /= len;
      for (a = 0; a < N; a++) bestd[a] = -1;
      for (a = 0; a < N; a++) bestw[a][0] = 0;
      //printf("here2\n");
      for (c = 0; c < words; c++) {
        a = 0;
        for (b = 0; b < cn; b++) if (bi[b] == c) a = 1;
        if (a == 1) continue;
        dist = 0;
        for (a = 0; a < size; a++) dist += vec[a] * M[a + c * size];
        for (a = 0; a < N; a++) {
          if (dist > bestd[a]) {
            for (d = N - 1; d > a; d--) {
              bestd[d] = bestd[d - 1];
              strcpy(bestw[d], bestw[d - 1]);
            }
            bestd[a] = dist;
            strcpy(bestw[a], &vocab[c * max_w]);
            break;
          }
        }
      }
      //printf("here3\n");
      // const char *underscore = strchr(file_name, '_');
      // const char *dot = strchr(underscore, '.');
      // size_t length = dot - (underscore + 1);
      // char extracted_string[length+1];
      // extracted_string[length] = '\0';
      // strncpy(extracted_string, underscore + 1, length);
      // char final_string[length + 8]; // "+3 for nw_, +4 for .txt"
      // snprintf(final_string, sizeof(final_string), "nw_%s.txt", extracted_string);
      // final_string[length+7] = '\0';
      // printf("here\n");
      // printf("%s\n", extracted_string);

      FILE *file;
      file = fopen(outfile, "a");

       if (file == NULL) {
        perror("Error opening file");
        return 1; // Exit with an error code
        }

      printf("here5\n");
      for (a = 0; a < N; a++){
        //printf("here6\n");
        fprintf(file, "%50s\t\t%f\n", bestw[a], bestd[a]);
        //char xx[]= "%50s\t\t%f\n", bestw[a], bestd[a];
        //fprintf(xx, file);
        //printf("here7\n");
      }
      fclose(file);
      printf("here8\n");
  //}
  }
  return 0;
}
