#!/usr/bin/env python
from tools.load import LoadMatrix
lm = LoadMatrix()
fm_train_real = lm.load_numbers('../data/fm_train_real.dat')
fm_test_real = lm.load_numbers('../data/fm_test_real.dat')
label_train_multiclass = lm.load_labels('../data/label_train_multiclass.dat')

parameter_list=[
		[ fm_train_real, fm_test_real, label_train_multiclass, 1.2, 1.2, 1e-5, 1, 0.001, 1.5],
		[ fm_train_real, fm_test_real, label_train_multiclass, 5, 1.2, 1e-2, 1, 0.001, 2]]

def mkl_multiclass (fm_train_real, fm_test_real, label_train_multiclass,
	width, C, epsilon, num_threads, mkl_epsilon, mkl_norm):

	from shogun import CombinedFeatures, MulticlassLabels
	from shogun import MKLMulticlass
	import shogun as sg

	kernel = sg.kernel("CombinedKernel")
	feats_train = CombinedFeatures()
	feats_test = CombinedFeatures()

	subkfeats_train = sg.features(fm_train_real)
	subkfeats_test = sg.features(fm_test_real)
	subkernel = sg.kernel("GaussianKernel", log_width=width)
	feats_train.append_feature_obj(subkfeats_train)
	feats_test.append_feature_obj(subkfeats_test)
	kernel.add("kernel_array", subkernel)

	subkfeats_train = sg.features(fm_train_real)
	subkfeats_test = sg.features(fm_test_real)
	subkernel = sg.kernel("LinearKernel")
	feats_train.append_feature_obj(subkfeats_train)
	feats_test.append_feature_obj(subkfeats_test)
	kernel.add("kernel_array", subkernel)

	subkfeats_train = sg.features(fm_train_real)
	subkfeats_test = sg.features(fm_test_real)
	subkernel = sg.kernel("PolyKernel", cache_size=10, degree=2)
	feats_train.append_feature_obj(subkfeats_train)
	feats_test.append_feature_obj(subkfeats_test)
	kernel.add("kernel_array", subkernel)

	kernel.init(feats_train, feats_train)

	labels = MulticlassLabels(label_train_multiclass)

	mkl = MKLMulticlass(C, kernel, labels)

	mkl.set_epsilon(epsilon);
	mkl.get_global_parallel().set_num_threads(num_threads)
	mkl.set_mkl_epsilon(mkl_epsilon)
	mkl.set_mkl_norm(mkl_norm)

	mkl.train()

	kernel.init(feats_train, feats_test)

	out =  mkl.apply().get_labels()
	return out

if __name__ == '__main__':
	print('mkl_multiclass')
	mkl_multiclass(*parameter_list[0])
