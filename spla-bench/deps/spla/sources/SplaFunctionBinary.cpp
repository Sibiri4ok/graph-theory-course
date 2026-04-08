/**********************************************************************************/
/* This file is part of spla project                                              */
/* https://github.com/JetBrains-Research/spla                                     */
/**********************************************************************************/
/* MIT License                                                                    */
/*                                                                                */
/* Copyright (c) 2021 JetBrains-Research                                          */
/*                                                                                */
/* Permission is hereby granted, free of charge, to any person obtaining a copy   */
/* of this software and associated documentation files (the "Software"), to deal  */
/* in the Software without restriction, including without limitation the rights   */
/* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      */
/* copies of the Software, and to permit persons to whom the Software is          */
/* furnished to do so, subject to the following conditions:                       */
/*                                                                                */
/* The above copyright notice and this permission notice shall be included in all */
/* copies or substantial portions of the Software.                                */
/*                                                                                */
/* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     */
/* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       */
/* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    */
/* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         */
/* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  */
/* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  */
/* SOFTWARE.                                                                      */
/**********************************************************************************/

#include <spla-cpp/SplaFunctionBinary.hpp>

const spla::RefPtr<spla::Type> &spla::FunctionBinary::GetA() const {
    return mA;
}

const spla::RefPtr<spla::Type> &spla::FunctionBinary::GetB() const {
    return mB;
}

const spla::RefPtr<spla::Type> &spla::FunctionBinary::GetC() const {
    return mC;
}

const std::string &spla::FunctionBinary::GetSource() const {
    return mSource;
}

bool spla::FunctionBinary::CanApply(const spla::TypedObject &a, const spla::TypedObject &b, const spla::TypedObject &c) const {
    return a.GetType() == GetA() &&
           b.GetType() == GetB() &&
           c.GetType() == GetC();
}

spla::RefPtr<spla::FunctionBinary> spla::FunctionBinary::Make(spla::RefPtr<spla::Type> a, spla::RefPtr<spla::Type> b, spla::RefPtr<spla::Type> c, std::string source, spla::Library &library) {
    return RefPtr<FunctionBinary>(new FunctionBinary(std::move(a), std::move(b), std::move(c), std::move(source), library));
}

spla::FunctionBinary::FunctionBinary(spla::RefPtr<spla::Type> a, spla::RefPtr<spla::Type> b, spla::RefPtr<spla::Type> c, std::string source, spla::Library &library)
    : Object(TypeName::FunctionBinary, library), mA(std::move(a)), mB(std::move(b)), mC(std::move(c)), mSource(std::move(source)) {
}
