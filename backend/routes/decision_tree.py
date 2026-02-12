from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models.decision_tree import DecisionTree, DecisionTreeNode
from backend.services.decision_tree_service import DecisionTreeService
import json
import numpy as np

decision_tree_bp = Blueprint('decision_tree', __name__)


@decision_tree_bp.route('/decision-tree', methods=['GET'])
def get_all_trees():
    trees = DecisionTree.query.all()
    return jsonify([tree.to_dict() for tree in trees])


@decision_tree_bp.route('/decision-tree/<int:tree_id>', methods=['GET'])
def get_tree(tree_id):
    tree = DecisionTree.query.get(tree_id)
    if not tree:
        return jsonify({'error': 'Decision tree not found'}), 404
    
    return jsonify(tree.to_dict())


@decision_tree_bp.route('/decision-tree', methods=['POST'])
def create_tree():
    data = request.json
    
    tree = DecisionTree(
        name=data.get('name'),
        description=data.get('description'),
        target_variable=data.get('target_variable'),
        algorithm=data.get('algorithm', 'gini'),
        max_depth=data.get('max_depth', 5),
        min_samples_split=data.get('min_samples_split', 2),
        min_samples_leaf=data.get('min_samples_leaf', 1),
        status='draft'
    )
    
    db.session.add(tree)
    db.session.commit()
    
    return jsonify(tree.to_dict()), 201


@decision_tree_bp.route('/decision-tree/<int:tree_id>', methods=['PUT'])
def update_tree(tree_id):
    tree = DecisionTree.query.get(tree_id)
    if not tree:
        return jsonify({'error': 'Decision tree not found'}), 404
    
    data = request.json
    
    if 'name' in data:
        tree.name = data['name']
    if 'description' in data:
        tree.description = data['description']
    if 'algorithm' in data:
        tree.algorithm = data['algorithm']
    if 'max_depth' in data:
        tree.max_depth = data['max_depth']
    if 'min_samples_split' in data:
        tree.min_samples_split = data['min_samples_split']
    if 'min_samples_leaf' in data:
        tree.min_samples_leaf = data['min_samples_leaf']
    
    db.session.commit()
    
    return jsonify(tree.to_dict())


@decision_tree_bp.route('/decision-tree/<int:tree_id>', methods=['DELETE'])
def delete_tree(tree_id):
    tree = DecisionTree.query.get(tree_id)
    if not tree:
        return jsonify({'error': 'Decision tree not found'}), 404
    
    db.session.delete(tree)
    db.session.commit()
    
    return jsonify({'message': 'Decision tree deleted successfully'})


@decision_tree_bp.route('/decision-tree/<int:tree_id>/train', methods=['POST'])
def train_tree(tree_id):
    tree = DecisionTree.query.get(tree_id)
    if not tree:
        return jsonify({'error': 'Decision tree not found'}), 404
    
    data = request.json
    training_data = data.get('training_data', [])
    features = data.get('features', [])
    
    if not training_data or not features:
        return jsonify({'error': 'Training data and features are required'}), 400
    
    X = np.array([[row[f] for f in features] for row in training_data])
    y = np.array([row[tree.target_variable] for row in training_data])
    
    tree_dict = DecisionTreeService.build_tree(
        X, y, features,
        max_depth=tree.max_depth,
        min_samples_split=tree.min_samples_split,
        min_samples_leaf=tree.min_samples_leaf,
        algorithm=tree.algorithm
    )
    
    DecisionTreeNode.query.filter_by(tree_id=tree_id).delete()
    
    def save_nodes(node_dict, parent_id=None, position_x=0, position_y=0):
        node = DecisionTreeNode(
            tree_id=tree_id,
            node_id=node_dict['node_id'],
            parent_id=parent_id,
            feature=node_dict.get('feature'),
            threshold=node_dict.get('threshold'),
            operator=node_dict.get('operator'),
            is_leaf=node_dict['is_leaf'],
            class_label=node_dict.get('class_label'),
            samples=node_dict['samples'],
            gini=node_dict.get('gini'),
            entropy=node_dict.get('entropy'),
            value=json.dumps(node_dict['value']),
            position_x=position_x,
            position_y=position_y
        )
        db.session.add(node)
        
        if 'left' in node_dict:
            save_nodes(node_dict['left'], node_dict['node_id'], position_x - 100, position_y + 100)
        if 'right' in node_dict:
            save_nodes(node_dict['right'], node_dict['node_id'], position_x + 100, position_y + 100)
    
    save_nodes(tree_dict)
    
    accuracy = DecisionTreeService.calculate_accuracy(tree_dict, X, y, features)
    tree.training_accuracy = accuracy
    tree.status = 'trained'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Tree trained successfully',
        'accuracy': accuracy,
        'tree': tree.to_dict()
    })


@decision_tree_bp.route('/decision-tree/<int:tree_id>/predict', methods=['POST'])
def predict(tree_id):
    tree = DecisionTree.query.get(tree_id)
    if not tree:
        return jsonify({'error': 'Decision tree not found'}), 404
    
    if tree.status != 'trained':
        return jsonify({'error': 'Tree must be trained before prediction'}), 400
    
    data = request.json
    input_data = data.get('input', {})
    
    tree_dict = build_tree_dict(tree.nodes)
    
    prediction = DecisionTreeService.predict(tree_dict, input_data)
    
    return jsonify({
        'prediction': prediction,
        'input': input_data
    })


def build_tree_dict(nodes):
    if not nodes:
        return None
    
    root_node = next((n for n in nodes if n.parent_id is None or n.node_id == '0'), nodes[0])
    
    def build_node(node):
        node_dict = {
            'node_id': node.node_id,
            'is_leaf': node.is_leaf,
            'samples': node.samples,
            'gini': node.gini,
            'entropy': node.entropy,
            'value': json.loads(node.value) if node.value else {}
        }
        
        if node.is_leaf:
            node_dict['class_label'] = node.class_label
        else:
            node_dict['feature'] = node.feature
            node_dict['threshold'] = node.threshold
            node_dict['operator'] = node.operator
            
            left_child = next((n for n in nodes if n.node_id == f"{node.node_id}-L"), None)
            right_child = next((n for n in nodes if n.node_id == f"{node.node_id}-R"), None)
            
            if left_child:
                node_dict['left'] = build_node(left_child)
            if right_child:
                node_dict['right'] = build_node(right_child)
        
        return node_dict
    
    return build_node(root_node)
