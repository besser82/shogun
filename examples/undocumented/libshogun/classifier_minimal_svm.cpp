#include <shogun/labels/BinaryLabels.h>
#include <shogun/features/DenseFeatures.h>
#include <shogun/kernel/GaussianKernel.h>
#include <shogun/classifier/svm/LibSVM.h>
#include <shogun/lib/common.h>
#include <shogun/io/SGIO.h>

using namespace shogun;

int main(int argc, char** argv)
{
	// create some data
	SGMatrix<float64_t> matrix(2,3);
	for (int32_t i=0; i<6; i++)
		matrix.matrix[i]=i;

	// create three 2-dimensional vectors
	// shogun will now own the matrix created
	auto features= std::make_shared<DenseFeatures<float64_t>>(matrix);

	// create three labels
	auto labels=std::make_shared<BinaryLabels>(3);
	labels->set_label(0, -1);
	labels->set_label(1, +1);
	labels->set_label(2, -1);

	// create gaussian kernel with cache 10MB, width 0.5
	auto kernel = std::make_shared<GaussianKernel>(10, 0.5);
	kernel->init(features, features);

	// create libsvm with C=10 and train
	auto svm = std::make_shared<LibSVM>(10, kernel, labels);
	svm->train();

	// classify on training examples
	for (int32_t i=0; i<3; i++)
		SG_SPRINT("output[%d]=%f\n", i, svm->apply_one(i));

	// free up memory

	return 0;
}
