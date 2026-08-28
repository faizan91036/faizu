"""
Storage module for managing persistent local storage of tasks.
Uses JSON format for storing tasks.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class TaskStorage:
    """Handles all storage operations for tasks."""
    
    def __init__(self, storage_dir: str = "data", filename: str = "tasks.json"):
        """
        Initialize storage handler.
        
        Args:
            storage_dir: Directory to store task data
            filename: Name of the JSON file
        """
        self.storage_dir = storage_dir
        self.storage_path = os.path.join(storage_dir, filename)
        
        # Create storage directory if it doesn't exist
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """
        Load tasks from local storage.
        
        Returns:
            List of task dictionaries
        """
        if not os.path.exists(self.storage_path):
            return []
        
        try:
            with open(self.storage_path, 'r') as f:
                tasks = json.load(f)
                return tasks if isinstance(tasks, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        """
        Save tasks to local storage.
        
        Args:
            tasks: List of task dictionaries to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(tasks, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def add_task(self, task_name: str) -> Dict[str, Any]:
        """
        Add a new task to storage.
        
        Args:
            task_name: Name/description of the task
            
        Returns:
            The created task dictionary
        """
        tasks = self.load_tasks()
        
        # Generate new ID
        task_id = max([t['id'] for t in tasks], default=0) + 1
        
        new_task = {
            'id': task_id,
            'name': task_name,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        tasks.append(new_task)
        self.save_tasks(tasks)
        
        return new_task
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """
        Update a task's properties.
        
        Args:
            task_id: ID of the task to update
            **kwargs: Properties to update
            
        Returns:
            True if successful, False otherwise
        """
        tasks = self.load_tasks()
        
        for task in tasks:
            if task['id'] == task_id:
                task.update(kwargs)
                if 'completed' in kwargs and kwargs['completed']:
                    task['completed_at'] = datetime.now().isoformat()
                self.save_tasks(tasks)
                return True
        
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from storage.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if successful, False otherwise
        """
        tasks = self.load_tasks()
        initial_length = len(tasks)
        tasks = [t for t in tasks if t['id'] != task_id]
        
        if len(tasks) < initial_length:
            self.save_tasks(tasks)
            return True
        
        return False
    
    def get_task(self, task_id: int) -> Dict[str, Any] | None:
        """
        Get a specific task by ID.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task dictionary or None if not found
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def clear_completed(self) -> int:
        """
        Remove all completed tasks.
        
        Returns:
            Number of tasks removed
        """
        tasks = self.load_tasks()
        initial_length = len(tasks)
        tasks = [t for t in tasks if not t['completed']]
        removed = initial_length - len(tasks)
        
        if removed > 0:
            self.save_tasks(tasks)
        
        return removed
