/**********************************************************************************/
/* Загрузка .mtx coordinate (pattern | integer | real) с весами для SSSP.         */
/* Повторяет семантику MtxLoader::load: 1-based->0-based, undirected, no loops. */
/**********************************************************************************/
#ifndef SPLA_MTX_LOAD_WEIGHTED_HPP
#define SPLA_MTX_LOAD_WEIGHTED_HPP

#include <spla.hpp>

#include <algorithm>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

namespace spla::examples {

    inline bool mtx_load_weighted(const std::filesystem::path&           file_path,
                                  bool                                   offset_indices,
                                  bool                                   make_undirected,
                                  bool                                   remove_loops,
                                  spla::uint&                            out_n_rows,
                                  spla::uint&                            out_n_cols,
                                  std::vector<spla::uint>&               out_Ai,
                                  std::vector<spla::uint>&               out_Aj,
                                  std::vector<float>&                    out_Ax) {

        std::ifstream file(file_path);
        if (!file) {
            std::cerr << "failed to open " << file_path << std::endl;
            return false;
        }

        std::string header_line;
        while (std::getline(file, header_line)) {
            if (!header_line.empty() && header_line[0] == '%') {
                continue;
            }
            break;
        }

        bool is_pattern = header_line.find("pattern") != std::string::npos;
        bool is_int     = header_line.find("integer") != std::string::npos;

        std::istringstream hdr(header_line);
        std::size_t        nrows = 0, ncols = 0, nnz = 0;
        hdr >> nrows >> ncols >> nnz;
        if (nrows == 0 || nnz == 0) {
            std::cerr << "invalid mtx header\n";
            return false;
        }

        out_n_rows = static_cast<spla::uint>(nrows);
        out_n_cols = static_cast<spla::uint>(ncols);

        struct Triple {
            spla::uint i, j;
            float      w;
        };
        std::vector<Triple> edges;
        edges.reserve(nnz * (make_undirected ? 2u : 1u));

        for (std::size_t k = 0; k < nnz; k++) {
            std::string line;
            if (!std::getline(file, line)) {
                std::cerr << "unexpected EOF in mtx data\n";
                return false;
            }
            if (line.empty()) {
                k--;
                continue;
            }
            if (line[0] == '%') {
                k--;
                continue;
            }
            std::istringstream ls(line);
            spla::uint         i0, j0;
            ls >> i0 >> j0;
            if (!ls) {
                std::cerr << "bad mtx line: " << line << std::endl;
                return false;
            }
            float w = 1.0f;
            if (!is_pattern) {
                if (is_int) {
                    int wi = 0;
                    ls >> wi;
                    w = static_cast<float>(wi);
                } else {
                    double wd = 0.0;
                    ls >> wd;
                    w = static_cast<float>(wd);
                }
            }

            spla::uint i = i0;
            spla::uint j = j0;
            if (offset_indices) {
                if (i == 0 || j == 0) {
                    std::cerr << "mtx indices must be >= 1 with offset_indices\n";
                    return false;
                }
                i -= 1;
                j -= 1;
            }
            if (remove_loops && i == j) {
                continue;
            }

            edges.push_back({i, j, w});
            if (make_undirected) {
                edges.push_back({j, i, w});
            }
        }

        std::sort(edges.begin(), edges.end(), [](const Triple& a, const Triple& b) {
            if (a.i != b.i) {
                return a.i < b.i;
            }
            if (a.j != b.j) {
                return a.j < b.j;
            }
            return a.w < b.w;
        });

        out_Ai.clear();
        out_Aj.clear();
        out_Ax.clear();
        out_Ai.reserve(edges.size());
        out_Aj.reserve(edges.size());
        out_Ax.reserve(edges.size());

        for (std::size_t k = 0; k < edges.size(); k++) {
            if (k > 0 && edges[k].i == edges[k - 1].i && edges[k].j == edges[k - 1].j) {
                continue;
            }
            out_Ai.push_back(edges[k].i);
            out_Aj.push_back(edges[k].j);
            out_Ax.push_back(edges[k].w);
        }

        std::cout << "Loaded weighted mtx: " << out_Ai.size() << " edges, " << out_n_rows << " rows\n";
        return true;
    }

}// namespace spla::examples

#endif
